# macOS Setup and Usage Guide

This folder contains shell scripts that allow macOS users to run the Multi-Camera Object Tracking System.

## Prerequisites

- macOS 10.14 (Mojave) or later
- Terminal application (built into macOS)
- Internet connection for downloading dependencies

## Quick Start

1. **Open Terminal** (Applications > Utilities > Terminal)

2. **Navigate to the project directory**:
   ```bash
   cd /path/to/Simple-Multi-Camera-Motion-Detection-master
   ```

3. **Make the scripts executable**:
   ```bash
   chmod +x mac/*.sh
   ```

4. **Run the setup script**:
   ```bash
   ./mac/setup_mac.sh
   ```

## Available Scripts

### `setup_mac.sh`
- **Purpose**: Initial setup and dependency installation
- **What it does**:
  - Installs Homebrew (macOS package manager) if not present
  - Installs Python3 and pip3
  - Creates a virtual environment
  - Installs required Python packages
- **When to use**: First time setup or when you need to reinstall dependencies

### `configure_cameras.sh`
- **Purpose**: Configure camera settings and test camera connections
- **What it does**:
  - Launches the camera configuration tool
  - Helps you set up camera parameters
  - Tests camera connectivity
- **When to use**: Before running the main application for the first time, or when you need to change camera settings

### `run_application.sh`
- **Purpose**: Launch the main multi-camera object tracking application
- **What it does**:
  - Performs comprehensive error checking
  - Activates the virtual environment
  - Launches the main application
- **When to use**: When you want to run the full application with your configured cameras

### `run_demo.sh`
- **Purpose**: Run the application in demo mode
- **What it does**:
  - Shows simulated camera feeds with moving objects
  - Useful for testing without real cameras
- **When to use**: For testing the system or when you don't have cameras connected

### `run.sh`
- **Purpose**: Simple launcher for the main application
- **What it does**:
  - Basic virtual environment activation
  - Camera availability check
  - Launches main.py
- **When to use**: Quick launch when you're confident everything is set up correctly

## Usage Workflow

1. **First time setup**:
   ```bash
   ./mac/setup_mac.sh
   ```

2. **Configure cameras**:
   ```bash
   ./mac/configure_cameras.sh
   ```

3. **Run the application**:
   ```bash
   ./mac/run_application.sh
   ```

## Troubleshooting

### Permission Denied Errors
If you get permission errors when running scripts:
```bash
chmod +x mac/*.sh
```

### Python Not Found
If Python3 is not found, the setup script will install it via Homebrew. If you prefer to install manually:
```bash
brew install python3
```

### Virtual Environment Issues
If the virtual environment is corrupted:
```bash
rm -rf venv
./mac/setup_mac.sh
```

### Camera Access Issues
macOS may require camera permissions. Go to:
- System Preferences > Security & Privacy > Privacy > Camera
- Enable access for Terminal or your Python application

### OpenCV Issues
If you encounter OpenCV-related errors:
```bash
source venv/bin/activate
pip3 uninstall opencv-python
pip3 install opencv-python-headless
```

## File Structure

```
mac/
├── README_MAC.md          # This file
├── setup_mac.sh          # Initial setup script
├── configure_cameras.sh   # Camera configuration
├── run_application.sh     # Main application launcher
├── run_demo.sh           # Demo mode launcher
└── run.sh                # Simple launcher
```

## Notes

- All scripts use `python3` instead of `python` to ensure compatibility
- The virtual environment is created in the project root directory
- Scripts include error checking and user-friendly messages
- Make sure to run scripts from the project root directory, not from within the `mac` folder

## Support

If you encounter issues:
1. Check that you're running scripts from the project root directory
2. Ensure all scripts are executable (`chmod +x mac/*.sh`)
3. Verify Python3 is installed and accessible
4. Check camera permissions in macOS System Preferences 