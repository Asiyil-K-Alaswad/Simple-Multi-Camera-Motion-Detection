# Batch Files for Easy Application Launching

This directory contains batch files that make it easy to run the Multi-Camera Object Tracking System on Windows.

## Available Batch Files

### 1. `configure_cameras.bat`
**Purpose**: Launches the camera configuration tool

**What it does**:
- Checks if Python is installed
- Activates virtual environment if present
- Runs the camera configuration interface
- Allows you to configure camera devices and URLs
- Saves configuration to `camera_config.json`

**Usage**:
```
Double-click configure_cameras.bat
```
or
```
configure_cameras.bat
```

### 2. `run_application.bat`
**Purpose**: Launches the main multi-camera object tracking application

**What it does**:
- Checks if Python is installed
- Activates virtual environment if present
- Checks if camera configuration exists
- Warns if no configuration is found
- Runs the main application with 3D visualization

**Usage**:
```
Double-click run_application.bat
```
or
```
run_application.bat
```

## Recommended Workflow

1. **First Time Setup**:
   ```
   1. Run configure_cameras.bat
   2. Configure your cameras in the GUI
   3. Save the configuration
   4. Run run_application.bat
   ```

2. **Subsequent Runs**:
   ```
   Run run_application.bat directly
   ```

## Features of the Batch Files

### Error Handling
- Checks if Python is installed and accessible
- Verifies required files exist
- Provides helpful error messages
- Pauses on errors so you can read the messages

### Virtual Environment Support
- Automatically detects and activates virtual environment
- Works with both system Python and virtual environments

### User-Friendly
- Clear status messages
- Progress indicators
- Helpful instructions
- Confirmation prompts when needed

### Safety Checks
- Validates file existence
- Warns about missing configuration
- Allows user to cancel if needed

## Troubleshooting

### "Python is not installed" Error
- Install Python from https://python.org
- Make sure Python is added to PATH during installation

### "launcher.py not found" Error
- Make sure you're running the batch file from the project directory
- Check that all project files are present

### "No camera configuration found" Warning
- Run `configure_cameras.bat` first to set up your cameras
- Or press 'Y' to continue with default settings

### Virtual Environment Issues
- If you have a virtual environment, make sure it's in the `venv` folder
- The batch files will automatically detect and activate it

## Manual Alternative

If you prefer to run the applications manually:

```bash
# Configure cameras
python launcher.py

# Run main application
python main.py
```

## Notes

- These batch files are designed for Windows systems
- They work with both Python 3.8+ and virtual environments
- The files include proper error handling and user feedback
- They maintain the separation between configuration and execution as designed 