#!/usr/bin/env python3
"""
Setup script for Multi-Camera Object Tracking System
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    return run_command("python -m venv venv", "Creating virtual environment")


def get_activation_command():
    """Get the appropriate activation command for the current platform."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def install_dependencies():
    """Install project dependencies."""
    # Determine the pip command based on platform
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Upgrade pip first using python -m pip
    if not run_command(f"{python_cmd} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install setuptools and wheel first
    if not run_command(f"{pip_cmd} install setuptools wheel", "Installing setuptools and wheel"):
        return False
    
    # Install dependencies
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")


def create_run_script():
    """Create a run script for easy execution."""
    if platform.system() == "Windows":
        script_content = """@echo off
echo Activating virtual environment...
call venv\\Scripts\\activate
echo Starting Multi-Camera Object Tracking System...
python main.py
pause
"""
        script_path = "run.bat"
    else:
        script_content = """#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo "Starting Multi-Camera Object Tracking System..."
python main.py
"""
        script_path = "run.sh"
        # Make the script executable
        os.chmod(script_path, 0o755)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✓ Created run script: {script_path}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("Multi-Camera Object Tracking System - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Create run script
    create_run_script()
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nTo run the application:")
    
    if platform.system() == "Windows":
        print("1. Double-click 'run.bat' or")
        print("2. Open command prompt and run:")
        print("   venv\\Scripts\\activate")
        print("   python main.py")
    else:
        print("1. Run './run.sh' or")
        print("2. Open terminal and run:")
        print("   source venv/bin/activate")
        print("   python main.py")
    
    print("\nMake sure you have two cameras connected before running the application.")
    print("You can modify camera settings in config.py if needed.")


if __name__ == "__main__":
    main() 