@echo off
echo 🚀 Starting Cartoony Downloader Pro...

if not exist .venv (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b
)

call .venv\Scripts\activate
python src/api.py
pause
