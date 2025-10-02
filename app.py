import asyncio
from typing import List, Optional
import chainlit as cl
from chainlit.types import ThreadDict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.runnables import RunnableConfig

from mcp_client.client import MCPClientManager
from agents.research_agent import create_research_agent
from utils.llm import get_llm
from utils.database import get_data_layer

_mcp_manager = None
_mcp_tools = None
_initialization_lock = asyncio.Lock()
_is_initialized = False

async def ensure_mcp_initialized():
    global _mcp_manager, _mcp_tools, _is_initialized
    
    if _is_initialized and _mcp_manager and _mcp_tools:
        return _mcp_manager, _mcp_tools
    
    async with _initialization_lock:
        if _is_initialized and _mcp_manager and _mcp_tools:
            return _mcp_manager, _mcp_tools
        
        if _mcp_manager is None:
            _mcp_manager = MCPClientManager()
        
        await _mcp_manager.initialize_all_servers()
        _mcp_tools = await _mcp_manager.get_all_tools()
        _is_initialized = True
        
        return _mcp_manager, _mcp_tools

@cl.data_layer
def init_data_layer():
    return get_data_layer()

@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    if username == "user" and password == "user":
        return cl.User(
            identifier="default_user", metadata={"role": "user", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    try:
        mcp_manager, tools = await ensure_mcp_initialized()
        
        llm = get_llm(temperature=0.7, streaming=True)
        agent = create_research_agent(tools, llm)
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("message_history", [])
        
        await cl.Message(
            content="✨ Ready! Ask me anything."
        ).send()
        
    except Exception as e:
        import traceback
        await cl.Message(
            content=f"❌ Error: {str(e)}\n```\n{traceback.format_exc()}\n```"
        ).send()

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    try:
        mcp_manager, tools = await ensure_mcp_initialized()
        
        llm = get_llm(temperature=0.7, streaming=True)
        agent = create_research_agent(tools, llm)
        
        cl.user_session.set("agent", agent)
        
        message_history = []
        if "steps" in thread:
            for step in thread["steps"]:
                if step.get("type") == "user_message":
                    message_history.append(HumanMessage(content=step.get("output", "")))
                elif step.get("type") in ["assistant_message", "run"]:
                    message_history.append(AIMessage(content=step.get("output", "")))
        
        cl.user_session.set("message_history", message_history)
        
    except Exception as e:
        import traceback
        await cl.Message(
            content=f"❌ Error resuming: {str(e)}\n```\n{traceback.format_exc()}\n```"
        ).send()

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
    pass

@cl.on_settings_update
async def on_settings_update(settings):
    pass
