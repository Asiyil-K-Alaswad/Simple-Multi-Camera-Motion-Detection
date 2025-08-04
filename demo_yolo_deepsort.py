"""
Demonstration script for YOLOv8 + DeepSORT multi-camera tracking
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

def demo_yolo_deepsort():
    """Demonstrate YOLOv8 + DeepSORT tracking with webcam."""
    
    print("🎥 YOLOv8 + DeepSORT Multi-Camera Tracking Demo")
    print("=" * 50)
    print(f"Model: {YOLO_MODEL}")
    print(f"Track classes: {TRACK_CLASSES}")
    print(f"Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
    print("Press 'q' to quit, 's' to save frame")
    print("=" * 50)
    
    # Initialize object tracker
    try:
        tracker = ObjectTracker()
        print("✓ Object tracker initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize object tracker: {e}")
        return False
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Could not open webcam")
        return False
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    print("✓ Webcam opened successfully")
    
    frame_count = 0
    start_time = time.time()
    save_frame = False
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✗ Failed to read frame from webcam")
                break
            
            # Resize frame to match configuration
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            
            # Create a second frame (simulate second camera)
            # In a real setup, this would be from a second camera
            frame2 = frame.copy()
            
            # Track objects
            tracked_objects = tracker.track_objects(frame, frame2)
            
            # Draw detections on frame
            frame_with_detections = tracker.draw_detections(frame, tracked_objects["camera1"])
            
            # Add performance info
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"Frame {frame_count}: {len(tracked_objects['camera1'])} objects tracked, FPS: {fps:.1f}")
            
            # Add FPS counter to frame
            cv2.putText(frame_with_detections, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame_with_detections, f"Objects: {len(tracked_objects['camera1'])}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('YOLOv8 + DeepSORT Demo', frame_with_detections)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Quitting demo...")
                break
            elif key == ord('s'):
                save_frame = True
                filename = f"demo_frame_{frame_count}.jpg"
                cv2.imwrite(filename, frame_with_detections)
                print(f"Frame saved as {filename}")
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"✗ Error during demo: {e}")
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Print final statistics
    end_time = time.time()
    total_time = end_time - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    print("\n" + "=" * 50)
    print("📊 Demo Statistics")
    print("=" * 50)
    print(f"Total frames processed: {frame_count}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average FPS: {avg_fps:.2f}")
    print(f"YOLOv8 model: {YOLO_MODEL}")
    print(f"Track classes: {TRACK_CLASSES}")
    print("=" * 50)
    
    return True

def demo_with_video_file(video_path):
    """Demonstrate with a video file instead of webcam."""
    
    print(f"🎬 YOLOv8 + DeepSORT Demo with video: {video_path}")
    print("=" * 50)
    
    # Initialize object tracker
    try:
        tracker = ObjectTracker()
        print("✓ Object tracker initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize object tracker: {e}")
        return False
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"✗ Could not open video file: {video_path}")
        return False
    
    print("✓ Video file opened successfully")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video reached")
                break
            
            # Resize frame to match configuration
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            
            # Create a second frame (simulate second camera)
            frame2 = frame.copy()
            
            # Track objects
            tracked_objects = tracker.track_objects(frame, frame2)
            
            # Draw detections on frame
            frame_with_detections = tracker.draw_detections(frame, tracked_objects["camera1"])
            
            # Add performance info
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"Frame {frame_count}: {len(tracked_objects['camera1'])} objects tracked, FPS: {fps:.1f}")
            
            # Display frame
            cv2.imshow('YOLOv8 + DeepSORT Video Demo', frame_with_detections)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting demo...")
                break
                
    except Exception as e:
        print(f"✗ Error during demo: {e}")
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Print final statistics
    end_time = time.time()
    total_time = end_time - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    print("\n" + "=" * 50)
    print("📊 Video Demo Statistics")
    print("=" * 50)
    print(f"Total frames processed: {frame_count}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average FPS: {avg_fps:.2f}")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Demo with video file
        video_path = sys.argv[1]
        success = demo_with_video_file(video_path)
    else:
        # Demo with webcam
        success = demo_yolo_deepsort()
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n❌ Demo failed. Please check the error messages above.") 