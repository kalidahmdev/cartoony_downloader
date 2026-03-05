@echo off
echo 🚀 Setting up Cartoony Downloader Pro...

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b
)

REM Activate virtual environment and install dependencies
echo 🛠️ Installing dependencies...
call .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium

REM Setup .env
if not exist .env (
    echo 🔑 Setting up .env...
    copy .env.example .env
)

echo.
echo 🎉 Setup complete!
echo To start the server, run: start.bat
echo.
pause
