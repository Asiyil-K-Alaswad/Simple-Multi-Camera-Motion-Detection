@echo off
echo Multi-Camera Object Tracking System
echo ===================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if cameras are available
echo Checking for cameras...
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera 0 available:', cap.isOpened()); cap.release(); cap = cv2.VideoCapture(1); print('Camera 1 available:', cap.isOpened()); cap.release()"

echo.
echo Starting application...
echo Press Ctrl+C to stop
echo.

REM Run the main application
python main.py

pause 