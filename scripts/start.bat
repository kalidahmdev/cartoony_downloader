@echo off
echo 🚀 Starting Cartoony Downloader Pro...

REM Navigate to the project root directory from the scripts folder
cd /d "%~dp0.."

if not exist .venv (
    echo ❌ Virtual environment not found. Please run scripts\setup.bat first.
    pause
    exit /b
)

call .venv\Scripts\activate
echo 🌍 Opening browser...
start http://127.0.0.1:8000
python src\api.py
pause
