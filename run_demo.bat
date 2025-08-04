@echo off
echo Multi-Camera Object Tracking System - Demo Mode
echo ===============================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting demo mode...
echo This will show simulated camera feeds with moving objects
echo Press Ctrl+C to stop
echo.

REM Run the demo
python test_demo.py

pause 