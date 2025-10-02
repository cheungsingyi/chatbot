@echo off
REM ==========================================================
REM Chatbot Launcher for Windows 11
REM ==========================================================

echo.
echo ====================================
echo    Chatbot3 Launcher
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [SETUP] Virtual environment not found. Creating one...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

echo [OK] Virtual environment found

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated

REM Check if dependencies are installed
python -c "import chainlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [SETUP] Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found
    echo.
    echo Please create a .env file with your API keys:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and add your ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

echo [OK] .env file exists

REM Initialize database if needed
if not exist "chatbot.db" (
    echo.
    echo [SETUP] Initializing database...
    python init_db.py
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize database
        pause
        exit /b 1
    )
    echo [OK] Database initialized
) else (
    echo [OK] Database exists
)

echo.
echo ====================================
echo    Starting Chatbot...
echo ====================================
echo.
echo The chatbot will open in your default browser
echo Press Ctrl+C to stop the chatbot
echo.

REM Start Chainlit application
chainlit run app.py -h

REM If chainlit exits with error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Chatbot stopped with an error
    pause
    exit /b 1
)
