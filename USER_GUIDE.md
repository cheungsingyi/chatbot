# Chatbot3 User Guide

## Quick Start

### First-Time Setup

1. **Copy the chatbot folder** to your local hard drive:
   ```
   C:\chatbot3\
   ```

2. **Run the installation checker**:
   - Double-click `install_check.bat`
   - This checks if Python and all requirements are met
   - Fix any errors reported before proceeding

3. **Configure your API key**:
   - Copy `.env.example` to `.env`
   - Open `.env` in Notepad
   - Replace `your-api-key-here` with your actual Anthropic API key
   - Save and close

4. **Launch the chatbot**:
   - Double-click `start.bat`
   - The chatbot will automatically:
     - Create a virtual environment (first time only)
     - Install dependencies (first time only)
     - Initialize the database (first time only)
     - Open in your default browser

## Using the Chatbot

### Starting a Conversation

1. The chatbot opens at `http://localhost:8001`
2. Type your message in the input box at the bottom
3. Press Enter or click Send
4. Wait for the assistant's response

### Conversation Features

**Persistent History**: All conversations are saved automatically. Your chat history persists even after:
- Closing the browser
- Restarting your computer
- Shutting down the chatbot

**Thread Management**: 
- Click the hamburger menu (☰) to view past conversations
- Click any thread to resume that conversation
- The assistant remembers context from earlier in the thread

**Research Agent**:
- Ask the assistant to research topics
- Example: "Research the latest developments in quantum computing"
- The assistant will use specialized tools to gather information

### Common Tasks

**Ask a Question**:
```
What is the capital of France?
```

**Request Research**:
```
Research recent advances in solar panel efficiency
```

**Continue Previous Conversation**:
1. Click the menu icon (☰)
2. Select a previous thread
3. Continue chatting

**Start Fresh Conversation**:
- Click "New Chat" or refresh the page

## Troubleshooting

### Chatbot Won't Start

**Problem**: `start.bat` shows Python errors

**Solution**:
1. Run `install_check.bat` first
2. Ensure Python 3.10+ is installed
3. Check that `.env` file exists with valid API key

### Browser Doesn't Open

**Problem**: Chatbot starts but browser doesn't open

**Solution**: Manually navigate to `http://localhost:8001`

### Database Locked Error

**Problem**: Error message about database being locked

**Solution**:
1. Close all browser windows
2. Press `Ctrl+C` in the command window
3. Wait 5 seconds
4. Restart with `start.bat`

### Missing Conversation History

**Problem**: Previous conversations not showing in sidebar

**Solution**:
1. Refresh the browser page
2. Check that `chatbot.db` file exists
3. Run `python test_persistence.py` to verify database

### API Key Errors

**Problem**: Error about missing or invalid API key

**Solution**:
1. Verify `.env` file exists (not `.env.example`)
2. Open `.env` and confirm `ANTHROPIC_API_KEY=sk-...` is present
3. Ensure API key starts with `sk-`
4. Restart the chatbot after making changes

## Stopping the Chatbot

1. Go to the command window running the chatbot
2. Press `Ctrl+C`
3. Wait for graceful shutdown
4. Close the command window

## Data Location

Your conversation data is stored in:
```
C:\chatbot3\chatbot.db
```

**Important**: Do not delete this file unless you want to lose all conversation history.

## Getting Help

If you encounter issues not covered in this guide:

1. Check the command window for error messages
2. Run `python test_persistence.py` to diagnose database issues
3. Contact your IT administrator
4. Include the error message and what you were doing when it occurred
