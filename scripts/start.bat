@echo off
echo 🚀 Starting Cartoony Downloader Pro...

REM Navigate to the project root directory from the scripts folder
cd /d "%~dp0.."

if not exist .venv (
    echo ❌ Virtual environment not found. 
    choice /c YN /m "Do you want to run setup.bat now"
    if errorlevel 2 exit /b
    if errorlevel 1 (
        scripts\setup.bat
    )
)

call .venv\Scripts\activate
echo 🌍 Opening browser...
start http://127.0.0.1:8000
python src\api.py
pause
