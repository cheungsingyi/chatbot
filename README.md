# AI Research Assistant with Chainlit + MCP + LangGraph

🚀 An intelligent AI chatbot built with Chainlit, integrating Model Context Protocol (MCP) servers and LangGraph agents for advanced research capabilities.

## 🌟 Features

- **🔌 MCP Integration**: Modular plugin system with 2 MCP servers (built with **FastMCP**)
  - **Confluence Mock Server**: Internal knowledge base (Engineering, Product, HR, Finance)
  - **Calculator Server**: Mathematical operations, unit conversions, statistics, date calculations

- **🤖 LangGraph Research Agent**: Intelligent agent with tool-calling capabilities
- **🎨 Interactive UI**: Real-time MCP server status display with streaming responses
- **🔒 Air-Gapped Ready**: Works without external internet access
- **⚡ OpenRouter LLM**: Powered by Grok-4-fast via OpenRouter
- **📦 FastMCP**: Modern decorator-based MCP server implementation (28% code reduction)

## 📁 Project Structure

```
chatbot3/
├── .env                      # Environment variables
├── .chainlit/
│   └── config.toml          # Chainlit + MCP configuration
├── mcp.json                 # MCP servers definition
├── requirements.txt         # Python dependencies
├── app.py                   # Main Chainlit application
├── mcp_client/
│   ├── client.py           # MCP client manager (MultiServerMCPClient)
│   └── servers/
│       ├── confluence_mock.py  # Mock Confluence MCP server (FastMCP)
│       └── calculator.py       # Calculator MCP server (FastMCP)
├── agents/
│   ├── research_agent.py   # LangGraph agent (create_react_agent)
│   └── config.py           # Agent configuration
└── utils/
    └── llm.py              # OpenRouter LLM setup (ChatOpenAI)
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
│                  MCP Integration Layer                          │
│  ┌────────────────────┐    ┌──────────────────────────┐    │
│  │ MultiServerMCP-    │    │  MCPClientManager        │    │
│  │ Client (high-level)│    │  - Connection config     │    │
│  │ (Tool Conversion)  │    │  - Multi-transport       │    │
│  └────────────────────┘    └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  MCP Servers Layer (FastMCP)                │
│  ┌──────────────────┐    ┌──────────────────────────┐      │
│  │ Confluence Mock  │    │  Calculator              │      │
│  │ (3 tools)        │    │  (4 tools)               │      │
│  │ @mcp.tool()      │    │  @mcp.tool()             │      │
│  └──────────────────┘    └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               OpenRouter LLM Provider                       │
│                 (x-ai/grok-4-fast:free)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Adding More MCP Servers

To add a new MCP server using FastMCP:

1. **Create the server** in `mcp_client/servers/your_server.py`:

```python
#!/usr/bin/env python3
from fastmcp import FastMCP

mcp = FastMCP("your-server")

@mcp.tool()
def your_tool(param: str) -> str:
    """What your tool does. This docstring becomes the tool description."""
    result = do_something(param)
    return result

if __name__ == "__main__":
    mcp.run()
```

2. **Register in mcp.json**:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "python",
      "args": ["mcp_client/servers/your_server.py"],
      "transport": "stdio",
      "description": "Your server description"
    }
  }
}
```

3. **Restart the application** - tools will be automatically loaded!

## 📚 Key Libraries & Patterns

### High-Level Abstractions Used

1. **FastMCP** (`mcp_client/servers/*.py`)
   - Modern decorator-based MCP server framework
   - Auto-generates JSON schemas from type hints
   - Docstrings become tool descriptions
   - Eliminated 199 lines of boilerplate (28% reduction)

2. **MultiServerMCPClient** (`mcp_client/client.py`)
   - From `langchain-mcp-adapters.client`
   - Manages multiple MCP server connections
   - Handles sessions and cleanup automatically
   - No manual context manager handling needed

3. **create_react_agent** (`agents/research_agent.py`)
   - From `langgraph.prebuilt`
   - Pre-built ReAct agent with tool calling
   - Handles reasoning and action loops

4. **LangchainCallbackHandler** (`app.py`)
   - Chainlit's built-in streaming handler
   - Real-time token streaming to UI
   - Automatic message formatting

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
- **langgraph>=0.2.0**: Agent orchestration (create_react_agent)
- **langchain>=0.3.0**: LLM framework
- **langchain-openai>=0.2.0**: OpenAI/OpenRouter integration
- **langchain-mcp-adapters>=0.1.0**: MCP to LangChain conversion (MultiServerMCPClient)
- **mcp>=1.0.0**: Model Context Protocol SDK
- **fastmcp>=2.12.0**: Modern decorator-based MCP server framework
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
