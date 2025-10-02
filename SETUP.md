# 🚀 Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment support

## Step-by-Step Installation

### 1. Navigate to Project Directory

```bash
cd /home/jack/coding_project/2025/chainlit/chatbot3
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: Installation may take 3-5 minutes as it includes LangChain, LangGraph, Chainlit, and MCP packages.

### 4. Verify Environment Configuration

Your `.env` file is already configured:

```bash
cat .env
```

Should show:
```
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=x-ai/grok-4-fast:free
```

### 5. Test MCP Servers (Optional)

Test the Confluence mock server:
```bash
python mcp_client/servers/confluence_mock.py
```

Test the calculator server:
```bash
python mcp_client/servers/calculator.py
```

Press `Ctrl+C` to stop each server after testing.

### 6. Start the Application

**Option A: Using the start script**
```bash
./start.sh
```

**Option B: Manual start**
```bash
chainlit run app.py -w
```

The `-w` flag enables auto-reload on file changes (useful for development).

### 7. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

You should see:
1. MCP servers initializing
2. Connection confirmation for both servers
3. List of available tools (7 total)
4. Ready message

## 🎯 Quick Test Queries

Try these queries to test the system:

### Test 1: Knowledge Search
```
Search for our API rate limits in Confluence
```

### Test 2: Calculation
```
Calculate: (450000 - 380000) / 380000 * 100
```

### Test 3: Combined Research
```
Find our Q4 revenue from Confluence and calculate the growth rate from Q3
```

### Test 4: Unit Conversion
```
Convert 100 requests per minute to requests per hour
```

### Test 5: Statistics
```
Calculate the mean of these team sizes: 8, 12, 6, 15, 9
```

## 🐛 Troubleshooting

### Issue: Import Errors

If you see import errors when starting:
```bash
pip install --upgrade langchain-mcp-adapters
pip install --upgrade chainlit
```

### Issue: MCP Server Not Starting

Check Python path in mcp.json. If using a different Python version:
```json
{
  "command": "python3",  // or "python3.10", "python3.11", etc.
  "args": ["mcp_client/servers/confluence_mock.py"]
}
```

### Issue: Port Already in Use

If port 8000 is busy:
```bash
chainlit run app.py -w --port 8001
```

### Issue: OpenRouter API Key

Verify your API key is loaded:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('OPENROUTER_API_KEY')[:20] + '...')"
```

### Issue: Module Not Found

Ensure you're in the project root and virtual environment is activated:
```bash
pwd  # Should show: /home/jack/coding_project/2025/chainlit/chatbot3
which python  # Should show: .../venv/bin/python
```

## 📊 Expected Behavior

### On Startup

```
🚀 Initializing AI Research Assistant...
📡 Connecting to MCP Servers...

🎯 MCP Servers Connected (2)
✅ confluence-mock
   📝 Internal company knowledge base (Confluence)
   🔧 python mcp_client/servers/confluence_mock.py

✅ calculator
   📝 Advanced calculator and data analysis tools
   🔧 python mcp_client/servers/calculator.py

🔧 Loading MCP tools...

🛠️ Available Tools (7 total)
confluence-mock: search_confluence, get_confluence_page, list_confluence_spaces
calculator: calculate, convert_units, statistics, date_calculator

✨ Ready! I'm your AI Research Assistant...
```

### During Query Processing

You'll see:
- Tool calls being made (search_confluence, calculate, etc.)
- Intermediate reasoning steps
- Final synthesized answer

## 🔄 Development Mode

For active development:

1. **Watch mode** (auto-reload on changes):
```bash
chainlit run app.py -w
```

2. **Debug mode**:
```bash
export CHAINLIT_DEBUG=true
chainlit run app.py -w
```

3. **Custom port**:
```bash
chainlit run app.py -w --port 8001
```

## 📦 Package Versions

Critical packages and their versions:

```bash
pip list | grep -E "(chainlit|langchain|langgraph|mcp)"
```

Expected output:
```
chainlit           1.3.0+
langchain          0.3.0+
langchain-core     0.3.0+
langchain-openai   0.2.0+
langgraph          0.2.0+
mcp                1.0.0+
```

## 🎓 Next Steps

1. **Explore the codebase**:
   - `app.py` - Main Chainlit application
   - `mcp_client/servers/` - MCP server implementations
   - `agents/` - LangGraph agent configuration

2. **Add your own MCP server**:
   - See README.md section "Adding More MCP Servers"

3. **Customize the agent**:
   - Edit `agents/config.py` for different behavior
   - Modify `agents/research_agent.py` for advanced patterns

4. **Deploy**:
   - Consider Docker containerization
   - Set up reverse proxy (nginx)
   - Configure authentication

## 📞 Support

If you encounter issues:
1. Check this guide
2. Review README.md
3. Inspect logs in terminal
4. Test MCP servers individually

---

**Happy researching! 🎉**
