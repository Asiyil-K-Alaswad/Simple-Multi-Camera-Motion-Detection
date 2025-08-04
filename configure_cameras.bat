@echo off
echo ========================================
echo Camera Configuration Tool
echo ========================================
echo.
echo Starting camera configuration...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "launcher.py" (
    echo ERROR: launcher.py not found in current directory
    echo Please run this batch file from the project directory.
    pause
    exit /b 1
)

REM Check if virtual environment exists and activate it if present
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
    echo.
)

REM Run the camera configuration tool
echo Starting camera configuration tool...
python launcher.py

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo ERROR: Camera configuration failed to start
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Camera configuration completed.
echo You can now run 'python main.py' to start the main application.
echo.
pause 