import os
import json
import asyncio
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.tools import BaseTool

class MCPClientManager:
    def __init__(self, config_path: str = "mcp.json"):
        self.config_path = config_path
        self.servers: Dict[str, Dict] = {}
        self.sessions: Dict[str, ClientSession] = {}
        self.stdio_contexts: Dict[str, Any] = {}
        self.session_contexts: Dict[str, Any] = {}
        self.tools: Dict[str, List[BaseTool]] = {}
        self._lock = asyncio.Lock()
        
    def load_config(self) -> Dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"MCP config not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        return config.get("mcpServers", {})
    
    async def connect_server(self, name: str, server_config: Dict):
        async with self._lock:
            if name in self.sessions:
                return {
                    "name": name,
                    "description": self.servers[name]["description"],
                    "status": "already_connected"
                }
            
            command = server_config.get("command", "python")
            args = server_config.get("args", [])
            description = server_config.get("description", "")
            
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=None
            )
            
            try:
                stdio_ctx = stdio_client(server_params)
                read, write = await stdio_ctx.__aenter__()
                
                session_ctx = ClientSession(read, write)
                session = await session_ctx.__aenter__()
                await session.initialize()
                
                self.servers[name] = {
                    "config": server_config,
                    "params": server_params,
                    "description": description
                }
                
                self.sessions[name] = session
                self.stdio_contexts[name] = stdio_ctx
                self.session_contexts[name] = session_ctx
                
                return {
                    "name": name,
                    "description": description,
                    "status": "connected"
                }
            except Exception as e:
                print(f"Failed to connect to {name}: {e}")
                raise
    
    async def initialize_all_servers(self):
        config = self.load_config()
        results = []
        
        for name, server_config in config.items():
            try:
                result = await self.connect_server(name, server_config)
                results.append(result)
            except Exception as e:
                results.append({
                    "name": name,
                    "description": server_config.get("description", ""),
                    "status": f"error: {str(e)}"
                })
        
        return results
    
    def get_server_info(self) -> List[Dict]:
        return [
            {
                "name": name,
                "description": info["description"],
                "command": info["config"]["command"],
                "args": " ".join(info["config"]["args"])
            }
            for name, info in self.servers.items()
        ]
    
    async def get_tools_from_server(self, name: str) -> List[BaseTool]:
        if name not in self.sessions:
            raise ValueError(f"Server not connected: {name}")
        
        session = self.sessions[name]
        
        from langchain_mcp_adapters.tools import load_mcp_tools
        tools = await load_mcp_tools(session)
        
        return tools
    
    async def get_all_tools(self) -> List[BaseTool]:
        all_tools = []
        
        for name in self.servers.keys():
            try:
                tools = await self.get_tools_from_server(name)
                self.tools[name] = tools
                all_tools.extend(tools)
            except Exception as e:
                print(f"Error loading tools from {name}: {e}")
        
        return all_tools
    
    async def cleanup(self):
        async with self._lock:
            for name in list(self.sessions.keys()):
                try:
                    if name in self.session_contexts:
                        await self.session_contexts[name].__aexit__(None, None, None)
                    if name in self.stdio_contexts:
                        await self.stdio_contexts[name].__aexit__(None, None, None)
                except Exception as e:
                    print(f"Error closing {name}: {e}")
            
            self.sessions.clear()
            self.stdio_contexts.clear()
            self.session_contexts.clear()
            self.servers.clear()
            self.tools.clear()
