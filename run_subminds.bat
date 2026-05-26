@echo off
REM SubMinds Desktop Application Launcher
REM Windows Batch Script

echo ========================================
echo SubMinds Desktop Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo.
        echo Please edit .env file with your IBM Cloud credentials
        echo Then run this script again.
        pause
        exit /b 1
    ) else (
        echo ERROR: .env.example not found!
        pause
        exit /b 1
    )
)

echo Configuration file found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: tkinter not available
    echo Please install tkinter for your Python version
    pause
    exit /b 1
)

echo Dependencies OK!
echo.

REM Run the application
echo Starting SubMinds Desktop Application...
echo.
python subminds_desktop.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo Application closed.
pause

@REM Made with Bob
