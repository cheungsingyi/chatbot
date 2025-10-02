#!/bin/bash

echo "🚀 Starting AI Research Assistant with MCP..."
echo ""

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

source venv/bin/activate

echo "✅ Environment activated"
echo "📦 Checking dependencies..."

pip show chainlit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Chainlit not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "🎯 Starting Chainlit application..."
echo "🌐 Access at: http://localhost:8000"
echo ""

chainlit run app.py -w
