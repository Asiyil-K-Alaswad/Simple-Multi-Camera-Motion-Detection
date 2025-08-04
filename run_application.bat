@echo off
echo ========================================
echo Multi-Camera Object Tracking System
echo ========================================
echo.
echo Starting main application...
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
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
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

REM Check if camera configuration exists
if not exist "camera_config.json" (
    echo WARNING: No camera configuration found.
    echo It is recommended to run configure_cameras.bat first.
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p choice=
    if /i not "%choice%"=="Y" (
        echo Cancelled by user.
        pause
        exit /b 0
    )
    echo.
)

REM Run the main application
echo Starting multi-camera object tracking system...
python main.py

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start or crashed
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Application completed successfully.
echo.
pause 