# 🎯 Quick Reference Card

## 📂 Project Structure

```
chatbot3/
├── .env                          # API keys (configured)
├── .env.example                  # Template
├── mcp.json                      # MCP server definitions
├── requirements.txt              # Dependencies
├── start.sh                      # Quick start script
├── app.py                        # Main Chainlit app
├── .chainlit/config.toml        # Chainlit + MCP config
├── mcp_client/
│   ├── client.py                # MCP client manager
│   └── servers/
│       ├── confluence_mock.py   # Knowledge base (3 tools)
│       └── calculator.py        # Math tools (4 tools)
├── agents/
│   ├── research_agent.py        # LangGraph agent
│   └── config.py                # Agent instructions
└── utils/
    └── llm.py                   # OpenRouter setup
```

## 🚀 Commands

```bash
# Start application
./start.sh

# OR manually
source venv/bin/activate
chainlit run app.py -w

# Test MCP server
python mcp_client/servers/confluence_mock.py

# Install dependencies
pip install -r requirements.txt
```

## 🛠️ Available Tools (7 total)

### Confluence Mock (3 tools)
- `search_confluence(query, space)` - Search knowledge base
- `get_confluence_page(page_id)` - Get full page
- `list_confluence_spaces()` - List all spaces

### Calculator (4 tools)
- `calculate(expression)` - Math expressions
- `convert_units(value, from, to)` - Unit conversion
- `statistics(numbers, operation)` - Stats analysis
- `date_calculator(date1, date2, operation)` - Date math

## 📚 Mock Data

### Confluence Spaces
- **Engineering**: API limits, architecture, deployment
- **Product**: Roadmap, features, analytics
- **HR**: Benefits, team structure (30 people, 5 teams)
- **Finance**: Q4 revenue $450K (+18.4% from Q3 $380K)

### Unit Conversions Supported
- **Length**: m, km, mile, foot, inch, yard
- **Weight**: kg, g, lb, oz
- **Time**: second, minute, hour, day, week
- **Data**: byte, kb, mb, gb, tb
- **Rate**: requests/second, requests/minute, requests/hour

### Statistics Operations
- mean, median, std, variance, min, max, sum

## 💬 Example Queries

### Knowledge Search
```
What are our API rate limits?
List all Confluence spaces
Get Q4 2024 roadmap details
```

### Calculations
```
Calculate: (450000 - 380000) / 380000 * 100
Calculate mean of: 8, 12, 6, 15, 9
What's 100 days from today?
```

### Unit Conversions
```
Convert 100 requests/minute to requests/hour
Convert 5 km to miles
Convert 1 GB to MB
```

### Combined Research
```
Find Q4 revenue and calculate growth rate from Q3
Search API limits and convert to requests per hour
Get team sizes and calculate average
```

## 🔧 Configuration

### .env
```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=x-ai/grok-4-fast:free
```

### mcp.json
```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["path/to/server.py"],
      "transport": "stdio",
      "description": "Server description"
    }
  }
}
```

### .chainlit/config.toml
```toml
[features.mcp.stdio]
enabled = true
allowed_executables = ["python", "python3"]

[features.mcp.sse]
enabled = true

[features.mcp.streamable-http]
enabled = true
```

## 🏗️ Key Components

### app.py
- `@cl.on_chat_start` - Initialize MCP + agent
- `@cl.on_message` - Handle user queries
- `@cl.on_settings_update` - Update settings

### mcp_client/client.py
- `MCPClientManager` - Manages MCP connections
- `load_config()` - Load mcp.json
- `get_all_tools()` - Convert to LangChain tools

### agents/research_agent.py
- `create_research_agent()` - Create LangGraph agent
- Uses `create_react_agent` pattern

### utils/llm.py
- `get_llm()` - OpenRouter LLM configuration
- Supports streaming and custom headers

## 📊 Architecture Flow

```
User Query
    ↓
Chainlit UI (app.py)
    ↓
LangGraph Agent (research_agent.py)
    ↓
Tool Selection & Execution
    ↓
MCP Client Manager (client.py)
    ↓
MCP Servers (confluence/calculator)
    ↓
Results back to User
```

## 🎨 UI Features

- Real-time MCP server status display
- Tool usage visualization
- Streaming responses
- Error handling
- Multi-step reasoning display

## 🔐 Security Notes

- Never commit .env to version control
- MCP stdio uses subprocess execution
- `allowed_executables` whitelist in config.toml
- No external internet access required

## 📈 Metrics

- **Response Time**: ~2-5 seconds (depends on LLM)
- **Tools**: 7 total (3 Confluence + 4 Calculator)
- **Mock Data**: 10 pages across 4 spaces
- **Supported Operations**: 20+ (search, calc, convert, stats, dates)

## 🐛 Quick Troubleshoots

| Issue | Solution |
|-------|----------|
| Import errors | `pip install --upgrade langchain-mcp-adapters` |
| Port in use | Use `--port 8001` |
| MCP not connecting | Check Python path in mcp.json |
| No response | Verify .env has OPENROUTER_API_KEY |
| Module not found | Activate venv: `source venv/bin/activate` |

## 📝 File Sizes (approximate)

- `app.py`: ~100 lines
- `mcp_client/client.py`: ~95 lines
- `confluence_mock.py`: ~200 lines
- `calculator.py`: ~220 lines
- Total project: ~800 lines of code

## 🎯 Success Indicators

On successful startup, you should see:
1. ✅ 2 MCP servers connected
2. ✅ 7 tools loaded
3. ✅ Agent initialized
4. ✅ Ready message

## 🚦 Status Codes

- ✅ Green: Server connected, tools loaded
- ⚠️ Yellow: Warning, partial functionality
- ❌ Red: Error, requires attention

---

**For detailed instructions, see:**
- SETUP.md - Installation guide
- README.md - Full documentation
- AGENTS.md - Agent guidelines

**Quick Start:** `./start.sh` → Open `http://localhost:8000` → Ask anything!
