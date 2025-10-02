import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv()

def get_llm(temperature: float = 0.7, streaming: bool = True):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4-fast:free")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment")
    
    return ChatOpenAI(
        model=model,
        api_key=SecretStr(api_key),
        base_url="https://openrouter.ai/api/v1",
        temperature=temperature,
        streaming=streaming,
        default_headers={
            "HTTP-Referer": "https://github.com/chainlit/chatbot",
            "X-Title": "Chainlit MCP Research Assistant"
        }
    )
