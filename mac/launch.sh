#!/bin/bash

# Universal launcher for macOS users
# This script can be run from anywhere and will automatically find the project directory

echo "========================================"
echo "Multi-Camera Object Tracking System"
echo "macOS Universal Launcher"
echo "========================================"
echo

# Find the project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Project directory found: $PROJECT_DIR"
echo

# Check if we're in the right place
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo "ERROR: Could not find main.py in the project directory."
    echo "Please ensure this script is in the 'mac' folder of the project."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Change to project directory
cd "$PROJECT_DIR"
echo "Changed to project directory: $(pwd)"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    echo
    ./mac/setup_mac.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please check the error messages above."
        echo
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

# Show menu
echo "========================================"
echo "What would you like to do?"
echo "========================================"
echo "1. Configure cameras"
echo "2. Run main application"
echo "3. Run demo mode"
echo "4. Setup/Reinstall dependencies"
echo "5. Exit"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Launching camera configuration..."
        ./mac/configure_cameras.sh
        ;;
    2)
        echo "Launching main application..."
        ./mac/run_application.sh
        ;;
    3)
        echo "Launching demo mode..."
        ./mac/run_demo.sh
        ;;
    4)
        echo "Running setup..."
        ./mac/setup_mac.sh
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac 