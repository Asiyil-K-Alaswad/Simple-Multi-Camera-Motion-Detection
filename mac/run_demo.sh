#!/bin/bash

echo "Multi-Camera Object Tracking System - Demo Mode"
echo "==============================================="
echo

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Warning: No virtual environment found. Using system Python."
fi

echo "Starting demo mode..."
echo "This will show simulated camera feeds with moving objects"
echo "Press Ctrl+C to stop"
echo

# Run the demo
python3 test_demo.py

echo
echo "Demo finished. Press Enter to continue..."
read 