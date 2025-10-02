@echo off
REM ==========================================================
REM Pre-flight Installation Checker
REM ==========================================================

echo.
echo ====================================
echo    Chatbot3 Installation Checker
echo ====================================
echo.

set ERROR_COUNT=0

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python is not installed or not in PATH
    echo        Install from: https://www.python.org/downloads/
    set /a ERROR_COUNT=%ERROR_COUNT%+1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [PASS] Python %PYTHON_VERSION% detected
)

REM Check Python version (3.10+)
echo [2/6] Checking Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python 3.10 or higher required
    set /a ERROR_COUNT=%ERROR_COUNT%+1
) else (
    echo [PASS] Python version is 3.10 or higher
)

REM Check pip installation
echo [3/6] Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] pip is not installed
    set /a ERROR_COUNT=%ERROR_COUNT%+1
) else (
    echo [PASS] pip is installed
)

REM Check if requirements.txt exists
echo [4/6] Checking requirements.txt...
if not exist "requirements.txt" (
    echo [FAIL] requirements.txt not found in current directory
    set /a ERROR_COUNT=%ERROR_COUNT%+1
) else (
    echo [PASS] requirements.txt found
)

REM Check if .env.example exists
echo [5/6] Checking .env.example...
if not exist ".env.example" (
    echo [WARN] .env.example not found
) else (
    echo [PASS] .env.example found
)

REM Check if .env exists
echo [6/6] Checking .env configuration...
if not exist ".env" (
    echo [WARN] .env file not found - you will need to create it
    echo        Copy .env.example to .env and add your API keys
) else (
    echo [PASS] .env file exists
    
    REM Check if API key is configured
    findstr /C:"ANTHROPIC_API_KEY=" .env >nul 2>&1
    if %errorlevel% neq 0 (
        echo [WARN] ANTHROPIC_API_KEY not found in .env
    ) else (
        findstr /C:"ANTHROPIC_API_KEY=sk-" .env >nul 2>&1
        if %errorlevel% neq 0 (
            echo [WARN] ANTHROPIC_API_KEY appears to be empty or invalid
        ) else (
            echo [PASS] ANTHROPIC_API_KEY is configured
        )
    )
)

echo.
echo ====================================
echo    Summary
echo ====================================

if %ERROR_COUNT% equ 0 (
    echo [SUCCESS] All critical checks passed!
    echo.
    echo You can now run start.bat to launch the chatbot
) else (
    echo [ERROR] %ERROR_COUNT% critical error(s) detected
    echo.
    echo Please fix the errors above before running start.bat
)

echo.
pause
