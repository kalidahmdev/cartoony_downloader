@echo off
setlocal
echo 🚀 Setting up Cartoony Downloader Pro...

REM Navigate to the project root directory from the scripts folder
cd /d "%~dp0.."

REM --- The Ultimate Python Finder ---
set "PYTHON_CMD="

REM 1. Check if 'python' works and isn't the dummy Windows Store app (which is usually 0 bytes)
python -c "import sys; print(sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    goto :python_found
)

REM 2. Check if 'python3' works
python3 -c "import sys; print(sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

REM 3. Check if 'py' works (Windows Python Launcher)
py -c "import sys; print(sys.version)" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
    goto :python_found
)

REM 4. Check common installation directories if it's not in PATH
REM Looks in AppData (User install) and Program Files (System install)
for /d %%i in ("%LocalAppData%\Programs\Python\Python3*", "%ProgramFiles%\Python3*", "%ProgramFiles(x86)%\Python3*") do (
    if exist "%%i\python.exe" (
        set "PYTHON_CMD=%%i\python.exe"
        goto :python_found
    )
)

:python_found
if "%PYTHON_CMD%"=="" (
    echo ❌ Python not found.
    echo Cartoony Downloader Pro requires Python 3.10+ to run.
    choice /c YN /m "Would you like me to automatically download and install Python 3.11 now"
    if errorlevel 2 (
        echo Please install Python manually from https://www.python.org/
        pause
        exit /b
    )
    if errorlevel 1 (
        echo 📥 Downloading and installing Python... (This may take a few minutes)
        winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
        if %errorlevel% neq 0 (
            echo ❌ Failed to automatically install Python. Please install it manually.
            pause
            exit /b
        )
        echo ✅ Python installed successfully! Please completely close this window and run scripts\setup.bat again.
        pause
        exit /b
    )
)

echo ✅ Found Python at: %PYTHON_CMD%
REM -----------------------------------

REM Create virtual environment in the project root
echo 📦 Creating virtual environment...
"%PYTHON_CMD%" -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b
)

REM Activate virtual environment and install dependencies from config/
echo 🛠️ Installing dependencies...
call .venv\Scripts\activate
"%PYTHON_CMD%" -m pip install -r config\requirements.txt
"%PYTHON_CMD%" -m playwright install chromium

REM Setup .env in the project root
if not exist .env (
    echo 🔑 Setting up .env...
    copy config\.env.example .env
)

echo.
echo 🎉 Setup complete!
echo.
choice /c YN /m "Do you want to start the server now"
if errorlevel 2 exit /b
if errorlevel 1 (
    scripts\start.bat
)
