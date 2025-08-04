"""
Main Application Entry Point

Multi-Camera Object Tracking System
"""

import sys
import os
import logging
import signal
import time
from typing import Optional

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from camera_manager import CameraManager
from object_tracker import ObjectTracker
from visualizer import Visualizer
from config import *

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multi_camera_tracking.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MultiCameraTrackingApp:
    """Main application class for multi-camera object tracking."""
    
    def __init__(self):
        """Initialize the application."""
        self.camera_manager = None
        self.object_tracker = None
        self.visualizer = None
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Multi-Camera Object Tracking Application initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def initialize(self) -> bool:
        """
        Initialize all application components.
        
        Returns:
            bool: True if initialization successful
        """
        try:
            logger.info("Initializing application components...")
            
            # Initialize camera manager
            self.camera_manager = CameraManager()
            if not self.camera_manager.initialize_cameras():
                logger.error("Failed to initialize cameras")
                return False
            
            # Initialize object tracker
            self.object_tracker = ObjectTracker()
            
            # Initialize visualizer
            self.visualizer = Visualizer(self.camera_manager, self.object_tracker)
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            return False
    
    def start(self):
        """Start the application."""
        try:
            if not self.initialize():
                logger.error("Failed to initialize application")
                return False
            
            self.running = True
            logger.info("Starting application...")
            
            # Start visualization (this will block until GUI is closed)
            self.visualizer.start()
            
            return True
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Error starting application: {e}")
            return False
    
    def stop(self):
        """Stop the application and cleanup resources."""
        try:
            logger.info("Stopping application...")
            self.running = False
            
            # Stop visualizer
            if self.visualizer:
                self.visualizer.stop()
            
            # Stop camera manager
            if self.camera_manager:
                self.camera_manager.stop_all()
            
            logger.info("Application stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping application: {e}")
    
    def run(self):
        """Main application run method."""
        try:
            success = self.start()
            if not success:
                logger.error("Application failed to start")
                return 1
            
            return 0
            
        except Exception as e:
            logger.error(f"Unexpected error in application: {e}")
            return 1
        finally:
            self.stop()


def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        import cv2
        import numpy
        import PIL
        import tkinter
        logger.info("All dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"Error: Missing dependency - {e}")
        print("Please install all dependencies using: pip install -r requirements.txt")
        return False


def check_cameras():
    """Check camera availability."""
    try:
        import cv2
        
        # Test camera 1
        cap1 = cv2.VideoCapture(CAMERA_1_INDEX)
        if cap1.isOpened():
            logger.info(f"Camera 1 (index {CAMERA_1_INDEX}) is available")
            cap1.release()
        else:
            logger.warning(f"Camera 1 (index {CAMERA_1_INDEX}) is not available")
        
        # Test camera 2
        cap2 = cv2.VideoCapture(CAMERA_2_INDEX)
        if cap2.isOpened():
            logger.info(f"Camera 2 (index {CAMERA_2_INDEX}) is available")
            cap2.release()
        else:
            logger.warning(f"Camera 2 (index {CAMERA_2_INDEX}) is not available")
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking cameras: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("Multi-Camera Object Tracking System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check cameras
    print("\nChecking camera availability...")
    check_cameras()
    
    # Create and run application
    app = MultiCameraTrackingApp()
    return app.run()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1) 