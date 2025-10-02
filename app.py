import asyncio
from typing import List, Optional
import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.runnables import RunnableConfig

from mcp_client.client import MCPClientManager
from agents.research_agent import create_research_agent
from utils.llm import get_llm

mcp_manager = MCPClientManager()

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="🚀 **Initializing AI Research Assistant...**"
    ).send()
    
    await cl.Message(
        content="📡 **Connecting to MCP Servers...**"
    ).send()
    
    try:
        server_results = await mcp_manager.initialize_all_servers()
        
        servers_info = mcp_manager.get_server_info()
        
        server_list = "\n".join([
            f"✅ **{s['name']}**\n   📝 {s['description']}\n   🔧 `{s['command']} {s['args']}`"
            for s in servers_info
        ])
        
        await cl.Message(
            content=f"## 🎯 MCP Servers Connected ({len(servers_info)})\n\n{server_list}"
        ).send()
        
        await cl.Message(
            content="🔧 **Loading MCP tools...**"
        ).send()
        
        tools = await mcp_manager.get_all_tools()
        
        tool_names = [t.name for t in tools]
        tools_list = ", ".join(tool_names)
        
        await cl.Message(
            content=f"## 🛠️ Available Tools ({len(tools)} total)\n\n{tools_list}"
        ).send()
        
        llm = get_llm(temperature=0.7, streaming=True)
        
        agent = create_research_agent(tools, llm)
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("mcp_manager", mcp_manager)
        cl.user_session.set("tools", tools)
        cl.user_session.set("message_history", [])
        
        await cl.Message(
            content="✨ **Ready! I'm your AI Research Assistant with access to internal knowledge and analytical tools.**\n\nAsk me anything like:\n- 'Search for our API rate limits and convert to requests per hour'\n- 'What's our Q4 revenue and growth rate?'\n- 'Find our team sizes and calculate the average'"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Error initializing MCP servers**: {str(e)}"
        ).send()
        raise

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    message_history: List[BaseMessage] = cl.user_session.get("message_history") or []
    
    if not agent:
        await cl.Message(
            content="❌ Agent not initialized. Please refresh the page."
        ).send()
        return
    
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        message_history.append(HumanMessage(content=message.content))
        
        config = RunnableConfig(
            callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)]
        )
        
        response = await agent.ainvoke(
            {"messages": message_history},
            config=config
        )
        
        if "messages" in response and len(response["messages"]) > 0:
            final_message = response["messages"][-1]
            
            if hasattr(final_message, "content"):
                msg.content = final_message.content
                message_history.append(AIMessage(content=final_message.content))
            else:
                msg.content = str(final_message)
                message_history.append(AIMessage(content=str(final_message)))
        else:
            msg.content = str(response)
            message_history.append(AIMessage(content=str(response)))
        
        cl.user_session.set("message_history", message_history)
        await msg.update()
        
    except Exception as e:
        msg.content = f"❌ **Error processing request**: {str(e)}\n\nTraceback: {e.__traceback__}"
        await msg.update()

@cl.on_chat_end
async def on_chat_end():
    await mcp_manager.cleanup()

@cl.on_settings_update
async def on_settings_update(settings):
    mcp_manager = cl.user_session.get("mcp_manager")
    
    if mcp_manager:
        servers_info = mcp_manager.get_server_info()
        await cl.Message(
            content=f"**Current MCP Servers**: {len(servers_info)} active"
        ).send()
