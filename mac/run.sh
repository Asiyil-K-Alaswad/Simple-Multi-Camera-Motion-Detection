#!/bin/bash

echo "Multi-Camera Object Tracking System"
echo "==================================="
echo

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Warning: No virtual environment found. Using system Python."
fi

# Check if cameras are available
echo "Checking for cameras..."
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera 0 available:', cap.isOpened()); cap.release(); cap = cv2.VideoCapture(1); print('Camera 1 available:', cap.isOpened()); cap.release()"

echo
echo "Starting application..."
echo "Press Ctrl+C to stop"
echo

# Run the main application
python3 main.py

echo
echo "Application finished. Press Enter to continue..."
read 