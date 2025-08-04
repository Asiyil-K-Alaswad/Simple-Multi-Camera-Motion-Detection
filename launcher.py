"""
Camera Configuration Launcher

Provides a camera configuration interface for setting up camera devices and URLs.
The main application should be started separately by running main.py.
"""

import sys
import os
import logging
from camera_config_ui import CameraConfigUI
from config import *

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the camera configuration launcher."""
    try:
        print("🔧 Camera Configuration Tool")
        print("=" * 50)
        print("Configure your camera setup before running the main application.")
        print("To start the main application, run: python main.py")
        print()
        
        # Start camera configuration interface
        config_ui = CameraConfigUI()
        config_ui.start()
        
    except KeyboardInterrupt:
        print("\n⚠️  Configuration interrupted by user")
    except Exception as e:
        logger.error(f"Error in camera configuration: {e}")
        print(f"❌ Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    # Check command line arguments
    success = True  # Default success value
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Camera Configuration Tool")
            print("=" * 40)
            print("Usage:")
            print("  python launcher.py          # Start camera configuration")
            print("  python launcher.py --help   # Show this help")
            print()
            print("After configuration, start the main application with:")
            print("  python main.py")
            print()
            print("Options:")
            print("  --help   Show this help message")
            success = True  # Help command is always successful
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
            success = False
    else:
        # Normal start with camera configuration
        success = main()
    
    if not success:
        sys.exit(1) 