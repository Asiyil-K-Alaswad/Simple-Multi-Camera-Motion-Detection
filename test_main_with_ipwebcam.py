#!/usr/bin/env python3
"""
Test script to verify main project works with IP webcam integration.
This script tests the updated camera manager and object tracker with URL cameras.
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
from object_tracker import ObjectTracker
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ipwebcam_integration():
    """Test IP webcam integration with main project components."""
    print("=" * 60)
    print("Testing IP Webcam Integration with Main Project")
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
        
        # Initialize object tracker
        print("\n2. Initializing Object Tracker...")
        object_tracker = ObjectTracker()
        print("✅ Object Tracker initialized successfully")
        
        # Test frame capture and object detection
        print("\n3. Testing Frame Capture and Object Detection...")
        print("Press 'q' to quit, 's' to save frame")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            try:
                # Get frames from cameras
                frame1, frame2 = camera_manager.get_frames()
                
                if frame1 is not None or frame2 is not None:
                    # Process frames with object tracking
                    if frame1 is not None and frame2 is not None:
                        # Both cameras available
                        tracked_objects = object_tracker.track_objects(frame1, frame2)
                        
                        # Draw detections
                        frame1_with_detections = object_tracker.draw_detections(frame1, tracked_objects["camera1"])
                        frame2_with_detections = object_tracker.draw_detections(frame2, tracked_objects["camera2"])
                        
                        # Display frames
                        cv2.imshow('Camera 1 (Main Project)', frame1_with_detections)
                        cv2.imshow('Camera 2 (IP Webcam)', frame2_with_detections)
                        
                        # Print detection info
                        if tracked_objects["camera1"] or tracked_objects["camera2"]:
                            print(f"\nFrame {frame_count}:")
                            if tracked_objects["camera1"]:
                                print(f"  Camera 1: {len(tracked_objects['camera1'])} objects")
                            if tracked_objects["camera2"]:
                                print(f"  Camera 2: {len(tracked_objects['camera2'])} objects")
                        
                    elif frame1 is not None:
                        # Only camera 1 available
                        detected_objects = object_tracker.detect_objects(frame1, "camera1")
                        tracked_objects = object_tracker._update_deepsort_tracking(frame1, detected_objects, "camera1")
                        frame1_with_detections = object_tracker.draw_detections(frame1, tracked_objects)
                        cv2.imshow('Camera 1 (Main Project)', frame1_with_detections)
                        
                        # Show status for camera 2
                        status_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                        cv2.putText(status_frame, "IP Webcam: No signal", (50, 240), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow('Camera 2 (IP Webcam)', status_frame)
                        
                    elif frame2 is not None:
                        # Only camera 2 available
                        detected_objects = object_tracker.detect_objects(frame2, "camera2")
                        tracked_objects = object_tracker._update_deepsort_tracking(frame2, detected_objects, "camera2")
                        frame2_with_detections = object_tracker.draw_detections(frame2, tracked_objects)
                        cv2.imshow('Camera 2 (IP Webcam)', frame2_with_detections)
                        
                        # Show status for camera 1
                        status_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                        cv2.putText(status_frame, "Camera 1: No signal", (50, 240), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow('Camera 1 (Main Project)', status_frame)
                    
                    frame_count += 1
                    
                    # Calculate and display FPS
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        fps = frame_count / elapsed_time
                        print(f"\rFPS: {fps:.1f} | Frame: {frame_count}", end="", flush=True)
                    
                else:
                    # No frames available
                    status_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(status_frame, "No camera signals", (50, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Camera 1 (Main Project)', status_frame)
                    cv2.imshow('Camera 2 (IP Webcam)', status_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n\nQuitting...")
                    break
                elif key == ord('s'):
                    # Save current frames
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    if frame1 is not None:
                        cv2.imwrite(f"main_test_camera1_{timestamp}.jpg", frame1)
                    if frame2 is not None:
                        cv2.imwrite(f"main_test_camera2_{timestamp}.jpg", frame2)
                    print(f"\nSaved frames as main_test_camera*_{timestamp}.jpg")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)
        
        # Cleanup
        cv2.destroyAllWindows()
        camera_manager.stop_all()
        
        print("\n✅ IP Webcam integration test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in IP webcam integration test: {e}")
        print(f"\n❌ IP Webcam integration test failed: {e}")
        return False

def main():
    """Main function."""
    print("Testing IP Webcam Integration with Main Project")
    print("This test verifies that the main project can handle URL cameras")
    print("Make sure your IP webcam is running and accessible")
    print("Camera configuration should be in camera_config.json")
    
    success = test_ipwebcam_integration()
    
    if success:
        print("\n🎉 All tests passed! The main project is ready for IP webcam use.")
        print("\nNext steps:")
        print("1. Run the main application: python main.py")
        print("2. The GUI will show both camera feeds with object tracking")
        print("3. IP webcam frames will be processed using the improved logic")
    else:
        print("\n❌ Tests failed. Please check your IP webcam configuration.")
        print("\nTroubleshooting:")
        print("1. Ensure IP webcam app is running")
        print("2. Check camera_config.json has correct URL")
        print("3. Verify network connectivity")
        print("4. Try the basic test: python test_ipwebcam_basic.py")

if __name__ == "__main__":
    main() 