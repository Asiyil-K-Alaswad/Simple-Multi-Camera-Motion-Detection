#!/bin/bash

echo "========================================"
echo "Multi-Camera Object Tracking System"
echo "========================================"
echo
echo "Starting main application..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python3 and try again."
    echo "You can install Python3 using Homebrew: brew install python3"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found in current directory"
    echo "Please run this script from the project directory."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists and activate it if present
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment activated."
    echo
else
    echo "Warning: No virtual environment found. Using system Python."
    echo
fi

# Check if camera configuration exists
if [ ! -f "camera_config.json" ]; then
    echo "WARNING: No camera configuration found."
    echo "It is recommended to run ./configure_cameras.sh first."
    echo
    read -p "Do you want to continue anyway? (y/N): " choice
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        echo "Cancelled by user."
        exit 0
    fi
    echo
fi

# Run the main application
echo "Starting multi-camera object tracking system..."
python3 main.py

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Application failed to start or crashed"
    echo "Please check the error messages above."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

echo
echo "Application completed successfully."
echo
read -p "Press Enter to continue..." 