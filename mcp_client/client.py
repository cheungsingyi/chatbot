import os
import json
from typing import Dict, List, Any
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPClientManager:
    def __init__(self, config_path: str = "mcp.json"):
        self.config_path = config_path
        self.client: MultiServerMCPClient | None = None
        self.server_configs: Dict[str, Dict] = {}
        self.tools: List[BaseTool] = []
        
    def load_config(self) -> Dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"MCP config not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        return config.get("mcpServers", {})
    
    def _build_connection_config(self, config: Dict) -> Dict[str, Any]:
        transport = config.get("transport", "stdio")
        
        if transport == "stdio":
            return {
                "transport": "stdio",
                "command": config.get("command", "python"),
                "args": config.get("args", [])
            }
        elif transport == "streamable_http":
            return {
                "transport": "streamable_http",
                "url": config["url"]
            }
        elif transport == "sse":
            return {
                "transport": "sse",
                "url": config["url"]
            }
        elif transport == "websocket":
            return {
                "transport": "websocket",
                "url": config["url"]
            }
        else:
            raise ValueError(f"Unsupported transport type: {transport}")
    
    async def initialize_all_servers(self):
        self.server_configs = self.load_config()
        
        connections = {
            name: self._build_connection_config(config)
            for name, config in self.server_configs.items()
        }
        
        try:
            self.client = MultiServerMCPClient(connections)  # type: ignore
            
            results = [
                {
                    "name": name,
                    "description": config.get("description", ""),
                    "status": "connected"
                }
                for name, config in self.server_configs.items()
            ]
            
            return results
        except Exception as e:
            return [
                {
                    "name": name,
                    "description": config.get("description", ""),
                    "status": f"error: {str(e)}"
                }
                for name, config in self.server_configs.items()
            ]
    
    def get_server_info(self) -> List[Dict]:
        return [
            {
                "name": name,
                "description": config.get("description", ""),
                "command": config.get("command", "python"),
                "args": " ".join(config.get("args", []))
            }
            for name, config in self.server_configs.items()
        ]
    
    async def get_all_tools(self) -> List[BaseTool]:
        if not self.client:
            raise RuntimeError("Client not initialized. Call initialize_all_servers first.")
        
        self.tools = await self.client.get_tools()
        return self.tools
    
    async def cleanup(self):
        self.client = None
        self.server_configs.clear()
        self.tools.clear()
