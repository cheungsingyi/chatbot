# agents/research_agent.py

```python
from typing import List
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from agents.config import RESEARCH_AGENT_INSTRUCTIONS

def create_research_agent(tools: List[BaseTool], llm):
    agent = create_react_agent(
        llm,
        tools,
        prompt=RESEARCH_AGENT_INSTRUCTIONS
    )
    
    return agent
```
