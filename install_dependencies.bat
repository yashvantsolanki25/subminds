@echo off
echo ========================================
echo SubMinds - Installing Dependencies
echo ========================================
echo.

REM Get the correct Python executable
python --version
echo.

echo Installing core dependencies...
python -m pip install --upgrade pip
python -m pip install opencv-python pillow python-dotenv numpy pyyaml requests

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the application:
echo   python subminds_app.py
echo.
pause

@REM Made with Bob
