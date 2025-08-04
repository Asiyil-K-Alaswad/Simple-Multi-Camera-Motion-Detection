#!/usr/bin/env python3
"""
Simple test script to verify camera frames are being captured correctly.
This script tests basic frame capture without object detection.
"""

import sys
import os
import logging
import time
import cv2
import numpy as np

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from camera_manager import CameraManager
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_camera_frames():
    """Test basic camera frame capture."""
    print("=" * 60)
    print("Testing Camera Frame Capture")
    print("=" * 60)
    
    try:
        # Initialize camera manager
        print("\n1. Initializing Camera Manager...")
        camera_manager = CameraManager()
        
        if not camera_manager.initialize_cameras():
            print("❌ Failed to initialize cameras")
            return False
        
        print("✅ Camera Manager initialized successfully")
        
        # Get camera info
        camera_info = camera_manager.get_camera_info()
        print(f"\nCamera Information:")
        for camera_id, info in camera_info.items():
            print(f"  {camera_id}: {info}")
        
        # Test frame capture
        print("\n2. Testing Frame Capture...")
        print("Press 'q' to quit, 's' to save frame")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            try:
                # Get frames from cameras
                frame1, frame2 = camera_manager.get_frames()
                
                # Display frames
                if frame1 is not None:
                    # Add info to frame1
                    cv2.putText(frame1, f"Camera 1 - Frame: {frame_count}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame1, f"Size: {frame1.shape[1]}x{frame1.shape[0]}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Camera 1 (Local)', frame1)
                else:
                    # Show status for camera 1
                    status_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(status_frame, "Camera 1: No signal", (50, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Camera 1 (Local)', status_frame)
                
                if frame2 is not None:
                    # Add info to frame2
                    cv2.putText(frame2, f"Camera 2 - Frame: {frame_count}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame2, f"Size: {frame2.shape[1]}x{frame2.shape[0]}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Camera 2 (IP Webcam)', frame2)
                else:
                    # Show status for camera 2
                    status_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(status_frame, "Camera 2: No signal", (50, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Camera 2 (IP Webcam)', status_frame)
                
                frame_count += 1
                
                # Calculate and display FPS
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    fps = frame_count / elapsed_time
                    print(f"\rFPS: {fps:.1f} | Frame: {frame_count} | Camera1: {'✓' if frame1 is not None else '✗'} | Camera2: {'✓' if frame2 is not None else '✗'}", end="", flush=True)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n\nQuitting...")
                    break
                elif key == ord('s'):
                    # Save current frames
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    if frame1 is not None:
                        cv2.imwrite(f"camera1_frame_{timestamp}.jpg", frame1)
                        print(f"\nSaved Camera 1 frame as: camera1_frame_{timestamp}.jpg")
                    if frame2 is not None:
                        cv2.imwrite(f"camera2_frame_{timestamp}.jpg", frame2)
                        print(f"Saved Camera 2 frame as: camera2_frame_{timestamp}.jpg")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)
        
        # Cleanup
        cv2.destroyAllWindows()
        camera_manager.stop_all()
        
        print("\n✅ Camera frame test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in camera frame test: {e}")
        print(f"\n❌ Camera frame test failed: {e}")
        return False

def main():
    """Main function."""
    print("Testing Camera Frame Capture")
    print("This test verifies that camera frames are being captured correctly")
    print("Make sure your cameras are connected and accessible")
    
    success = test_camera_frames()
    
    if success:
        print("\n🎉 Camera frames are working correctly!")
        print("\nNext steps:")
        print("1. If frames are showing, the issue is with object detection")
        print("2. If frames are not showing, check camera connections")
        print("3. Run the main application: python main.py")
    else:
        print("\n❌ Camera frame test failed.")
        print("\nTroubleshooting:")
        print("1. Check camera connections")
        print("2. Verify camera_config.json settings")
        print("3. Try different camera indices")

if __name__ == "__main__":
    main() 