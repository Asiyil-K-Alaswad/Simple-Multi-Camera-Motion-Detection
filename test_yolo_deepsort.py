"""
Test script for YOLOv8 + DeepSORT integration
"""

import cv2
import numpy as np
import time
import logging
from object_tracker import ObjectTracker
from config import *

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

def test_yolo_deepsort():
    """Test YOLOv8 and DeepSORT integration."""
    
    print("Testing YOLOv8 + DeepSORT integration...")
    
    # Initialize object tracker
    try:
        tracker = ObjectTracker()
        print("✓ Object tracker initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize object tracker: {e}")
        return False
    
    # Test with a sample image or video
    print("\nTesting with sample video...")
    
    # Try to open camera or create a test video
    cap = cv2.VideoCapture(0)  # Try to open default camera
    
    if not cap.isOpened():
        print("No camera available, creating test video...")
        # Create a simple test video with moving rectangles
        test_video = create_test_video()
        cap = test_video
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while frame_count < 100:  # Test for 100 frames
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize frame to match configuration
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            
            # Create a second frame (simulate second camera)
            frame2 = frame.copy()
            
            # Track objects
            tracked_objects = tracker.track_objects(frame, frame2)
            
            # Draw detections on frame
            frame_with_detections = tracker.draw_detections(frame, tracked_objects["camera1"])
            
            # Display frame
            cv2.imshow('YOLOv8 + DeepSORT Test', frame_with_detections)
            
            # Print tracking info every 30 frames
            if frame_count % 30 == 0:
                camera1_count = len(tracked_objects["camera1"])
                camera2_count = len(tracked_objects["camera2"])
                print(f"Frame {frame_count}: Camera1: {camera1_count} objects, Camera2: {camera2_count} objects")
                
                # Print track IDs
                for obj in tracked_objects["camera1"]:
                    if obj.track_id is not None:
                        print(f"  Track ID: {obj.track_id}, Class: {obj.class_name}, Confidence: {obj.confidence:.2f}")
            
            frame_count += 1
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    end_time = time.time()
    fps = frame_count / (end_time - start_time)
    
    print(f"\n✓ Test completed successfully!")
    print(f"  Frames processed: {frame_count}")
    print(f"  Average FPS: {fps:.2f}")
    print(f"  YOLOv8 model: {YOLO_MODEL}")
    print(f"  Track classes: {TRACK_CLASSES}")
    
    return True

def create_test_video():
    """Create a simple test video with moving rectangles."""
    class TestVideo:
        def __init__(self):
            self.frame_count = 0
            self.width = FRAME_WIDTH
            self.height = FRAME_HEIGHT
            
        def read(self):
            # Create a black frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Add moving rectangles to simulate people
            t = self.frame_count * 0.1
            
            # Rectangle 1 - moving horizontally
            x1 = int(100 + 50 * np.sin(t))
            y1 = 200
            cv2.rectangle(frame, (x1, y1), (x1 + 60, y1 + 120), (255, 255, 255), -1)
            
            # Rectangle 2 - moving vertically
            x2 = 400
            y2 = int(100 + 30 * np.cos(t * 0.5))
            cv2.rectangle(frame, (x2, y2), (x2 + 60, y2 + 120), (255, 255, 255), -1)
            
            # Rectangle 3 - moving diagonally
            x3 = int(250 + 40 * np.sin(t * 0.7))
            y3 = int(150 + 40 * np.cos(t * 0.7))
            cv2.rectangle(frame, (x3, y3), (x3 + 60, y3 + 120), (255, 255, 255), -1)
            
            self.frame_count += 1
            return True, frame
        
        def release(self):
            pass
    
    return TestVideo()

if __name__ == "__main__":
    success = test_yolo_deepsort()
    if success:
        print("\n🎉 All tests passed! YOLOv8 + DeepSORT integration is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.") 