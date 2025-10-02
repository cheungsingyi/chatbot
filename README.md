# AI Research Assistant with Chainlit + MCP + LangGraph

🚀 An intelligent AI chatbot built with Chainlit, integrating Model Context Protocol (MCP) servers and LangGraph agents for advanced research capabilities.

## 🌟 Features

- **🔌 MCP Integration**: Modular plugin system with 2 MCP servers
  - **Confluence Mock Server**: Internal knowledge base (Engineering, Product, HR, Finance)
  - **Calculator Server**: Mathematical operations, unit conversions, statistics, date calculations

- **🤖 LangGraph Research Agent**: Intelligent agent with tool-calling capabilities
- **🎨 Interactive UI**: Real-time MCP server status display
- **🔒 Air-Gapped Ready**: Works without external internet access
- **⚡ OpenRouter LLM**: Powered by Grok-4-fast via OpenRouter

## 📁 Project Structure

```
chatbot3/
├── .env                      # Environment variables
├── .chainlit/
│   └── config.toml          # Chainlit + MCP configuration
├── mcp.json                 # MCP servers definition
├── requirements.txt         # Python dependencies
├── app.py                   # Main Chainlit application
├── mcp/
│   ├── client.py           # MCP client manager
│   └── servers/
│       ├── confluence_mock.py  # Mock Confluence MCP server
│       └── calculator.py       # Calculator MCP server
├── agents/
│   ├── research_agent.py   # LangGraph agent
│   └── config.py           # Agent configuration
└── utils/
    └── llm.py              # OpenRouter LLM setup
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd /home/jack/coding_project/2025/chainlit/chatbot3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

The `.env` file is already configured with your OpenRouter credentials:

```bash
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=x-ai/grok-4-fast:free
```

### 3. Run the Application

```bash
chainlit run app.py -w
```

The application will start at `http://localhost:8000`

## 🛠️ MCP Servers

### Confluence Mock Server

Provides access to internal knowledge base with 4 spaces:

**Engineering Space:**
- API Rate Limits
- Architecture Overview  
- Deployment Runbook

**Product Space:**
- Q4 2024 Roadmap
- Feature: User Analytics

**HR Space:**
- Employee Benefits
- Team Structure

**Finance Space:**
- Q4 2024 Revenue

**Available Tools:**
- `search_confluence(query, space)` - Search for information
- `get_confluence_page(page_id)` - Get full page content
- `list_confluence_spaces()` - List all spaces

### Calculator Server

Advanced mathematical and analytical capabilities:

**Available Tools:**
- `calculate(expression)` - Evaluate math expressions
- `convert_units(value, from_unit, to_unit)` - Unit conversions
  - Length: m, km, mile, foot, inch
  - Weight: kg, g, lb, oz
  - Time: second, minute, hour, day
  - Data: byte, kb, mb, gb, tb
  - Rate: requests/second, requests/minute, requests/hour
- `statistics(numbers, operation)` - Statistical analysis
  - Operations: mean, median, std, variance, min, max, sum
- `date_calculator(date1, date2, operation)` - Date math
  - Operations: difference, add_days, subtract_days

## 💡 Example Usage

### Example 1: Financial Research with Calculations

```
User: "What was our Q4 revenue and what's the growth rate from Q3?"

Agent:
1. Searches Confluence for Q4 revenue data
2. Extracts Q4: $450,000 and Q3: $380,000
3. Uses calculator: (450000 - 380000) / 380000 * 100 = 18.4%
4. Reports: "Q4 2024 revenue was $450,000, representing 18.4% growth over Q3"
```

### Example 2: Technical Research with Unit Conversion

```
User: "Find our API rate limits and convert to requests per hour"

Agent:
1. Searches Engineering space for API limits
2. Finds: 100 requests/minute
3. Converts: 100 req/min → 6,000 req/hour
4. Reports: "REST API limit is 100 requests/minute (6,000 requests/hour)"
```

### Example 3: Team Analytics

```
User: "Get team sizes from HR and calculate the average"

Agent:
1. Searches HR space for team structure
2. Extracts team sizes: [8, 12, 6, 15, 9]
3. Calculates mean: 10
4. Reports: "5 teams with average size of 10 members"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Chainlit UI Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Chat Interface│  │ MCP Panel UI │  │ Server Status   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Agent Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   ReAct Agent with Tool Calling                      │   │
│  │   - Reasoning and Acting                             │   │
│  │   - Multi-step research workflows                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              MCP Integration Layer                          │
│  ┌────────────────────┐    ┌──────────────────────────┐    │
│  │ langchain-mcp-     │    │  MCPClientManager        │    │
│  │ adapters           │    │  - Connection handling   │    │
│  │ (Tool Conversion)  │    │  - Session management    │    │
│  └────────────────────┘    └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  MCP Servers Layer                          │
│  ┌──────────────────┐    ┌──────────────────────────┐      │
│  │ Confluence Mock  │    │  Calculator              │      │
│  │ (3 tools)        │    │  (4 tools)               │      │
│  └──────────────────┘    └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               OpenRouter LLM Provider                       │
│                 (x-ai/grok-4-fast:free)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Adding More MCP Servers

To add a new MCP server:

1. **Create the server** in `mcp/servers/your_server.py`:

```python
#!/usr/bin/env python3
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("your-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="your_tool",
            description="What your tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Parameter"}
                },
                "required": ["param"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "your_tool":
        result = do_something(arguments["param"])
        return [TextContent(type="text", text=result)]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

2. **Register in mcp.json**:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "python",
      "args": ["mcp/servers/your_server.py"],
      "transport": "stdio",
      "description": "Your server description"
    }
  }
}
```

3. **Restart the application** - tools will be automatically loaded!

## 🐛 Troubleshooting

### MCP Server Connection Issues

```bash
# Test individual MCP servers
python mcp/servers/confluence_mock.py
python mcp/servers/calculator.py
```

### LangChain MCP Adapters

If you encounter issues with `langchain-mcp-adapters`, ensure you have the latest version:

```bash
pip install --upgrade langchain-mcp-adapters
```

### OpenRouter API Issues

Verify your API key is set correctly:

```bash
echo $OPENROUTER_API_KEY
```

## 📚 Dependencies

- **chainlit>=1.3.0**: UI framework
- **langgraph>=0.2.0**: Agent orchestration
- **langchain>=0.3.0**: LLM framework
- **langchain-openai>=0.2.0**: OpenAI/OpenRouter integration
- **langchain-mcp-adapters>=0.1.0**: MCP to LangChain conversion
- **mcp>=1.0.0**: Model Context Protocol
- **python-dotenv**: Environment management
- **numpy**: Numerical computing
- **python-dateutil**: Date parsing

## 🎯 Future Enhancements

- [ ] Add real Confluence API integration
- [ ] Implement Jira MCP server
- [ ] Add Slack MCP server for team communication
- [ ] Enable persistent conversation history
- [ ] Add authentication and authorization
- [ ] Deploy with Docker

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! This is a POC demonstrating MCP integration patterns with Chainlit and LangGraph.

---

**Built with ❤️ using Chainlit, LangGraph, and Model Context Protocol**
