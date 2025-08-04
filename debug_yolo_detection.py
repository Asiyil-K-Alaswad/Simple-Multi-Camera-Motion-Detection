"""
Debug script for YOLO detection issues
"""

import cv2
import numpy as np
import time
import logging
from object_tracker import ObjectTracker
from config import *
from ultralytics import YOLO

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def debug_yolo_detection():
    """Debug YOLO detection step by step."""
    
    print("🔍 YOLO Detection Debug")
    print("=" * 50)
    print(f"Model: {YOLO_MODEL}")
    print(f"Confidence threshold: {YOLO_CONF_THRESHOLD}")
    print(f"IoU threshold: {YOLO_IOU_THRESHOLD}")
    print(f"Track classes: {TRACK_CLASSES}")
    print(f"Min object size: {MIN_OBJECT_SIZE}")
    print(f"Max object size: {MAX_OBJECT_SIZE}")
    print("=" * 50)
    
    # Test 1: Direct YOLO model test
    print("\n1. Testing YOLO model directly...")
    try:
        yolo_model = YOLO(YOLO_MODEL)
        print(f"✓ YOLO model loaded: {YOLO_MODEL}")
        print(f"Available classes: {list(yolo_model.names.values())}")
        
        # Test with a simple image
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 128  # Gray image
        results = yolo_model(test_image, conf=0.1, verbose=False)  # Lower confidence for testing
        
        print(f"✓ YOLO model inference works")
        print(f"Results type: {type(results)}")
        print(f"Number of results: {len(results)}")
        
    except Exception as e:
        print(f"✗ YOLO model test failed: {e}")
        return False
    
    # Test 2: Object tracker initialization
    print("\n2. Testing object tracker initialization...")
    try:
        tracker = ObjectTracker()
        print("✓ Object tracker initialized")
        print(f"YOLO model in tracker: {tracker.yolo_model is not None}")
        print(f"DeepSORT trackers: {len(tracker.trackers)}")
        
    except Exception as e:
        print(f"✗ Object tracker initialization failed: {e}")
        return False
    
    # Test 3: Test with webcam or create test image
    print("\n3. Testing with camera/video...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No camera available, creating test image...")
        # Create a test image with a person-like shape
        test_image = create_test_person_image()
        cap = None
    else:
        print("Camera available, using live feed...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    frame_count = 0
    max_frames = 50
    
    try:
        while frame_count < max_frames:
            if cap is not None:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            else:
                frame = test_image.copy()
                # Add some variation to the test image
                cv2.rectangle(frame, (100 + frame_count, 200), (160 + frame_count, 320), (255, 255, 255), -1)
            
            # Test direct YOLO detection
            print(f"\nFrame {frame_count + 1}:")
            print(f"Frame shape: {frame.shape}")
            print(f"Frame dtype: {frame.dtype}")
            print(f"Frame range: {frame.min()} - {frame.max()}")
            
            # Direct YOLO test
            direct_results = yolo_model(frame, conf=0.1, verbose=False)
            direct_detections = 0
            for result in direct_results:
                if result.boxes is not None:
                    direct_detections += len(result.boxes)
                    for box in result.boxes:
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = yolo_model.names[class_id]
                        confidence = float(box.conf[0].cpu().numpy())
                        print(f"  Direct YOLO: {class_name} (conf: {confidence:.2f})")
            
            print(f"  Direct YOLO detections: {direct_detections}")
            
            # Test through object tracker
            frame2 = frame.copy()  # Simulate second camera
            tracked_objects = tracker.track_objects(frame, frame2)
            
            camera1_count = len(tracked_objects["camera1"])
            camera2_count = len(tracked_objects["camera2"])
            
            print(f"  Tracker detections - Camera1: {camera1_count}, Camera2: {camera2_count}")
            
            # Show detections
            for obj in tracked_objects["camera1"]:
                print(f"    Tracked: {obj.class_name} (conf: {obj.confidence:.2f}) ID: {obj.track_id}")
            
            # Display frame with detections
            frame_with_detections = tracker.draw_detections(frame, tracked_objects["camera1"])
            cv2.imshow('YOLO Debug', frame_with_detections)
            
            frame_count += 1
            
            # Break on 'q' key
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
    
    print("\n" + "=" * 50)
    print("📊 Debug Summary")
    print("=" * 50)
    print(f"Frames tested: {frame_count}")
    print("=" * 50)
    
    return True

def create_test_person_image():
    """Create a test image with a person-like shape."""
    image = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    
    # Add background
    image[:] = (50, 50, 50)
    
    # Add a person-like shape (rectangle)
    cv2.rectangle(image, (200, 150), (260, 350), (255, 255, 255), -1)
    
    # Add head
    cv2.circle(image, (230, 120), 30, (255, 255, 255), -1)
    
    # Add some noise to make it more realistic
    noise = np.random.randint(0, 30, image.shape, dtype=np.uint8)
    image = cv2.add(image, noise)
    
    return image

def test_yolo_classes():
    """Test what classes YOLO can detect."""
    print("\n🔍 Testing YOLO Classes")
    print("=" * 30)
    
    try:
        yolo_model = YOLO(YOLO_MODEL)
        print(f"Model: {YOLO_MODEL}")
        print(f"Total classes: {len(yolo_model.names)}")
        
        # Show all available classes
        print("\nAvailable classes:")
        for i, name in yolo_model.names.items():
            print(f"  {i}: {name}")
        
        # Check if our target classes are available
        print(f"\nTarget classes: {TRACK_CLASSES}")
        for target_class in TRACK_CLASSES:
            if target_class in yolo_model.names.values():
                print(f"✓ '{target_class}' is available")
            else:
                print(f"✗ '{target_class}' is NOT available")
                
    except Exception as e:
        print(f"Error testing classes: {e}")

def test_different_confidence_thresholds():
    """Test detection with different confidence thresholds."""
    print("\n🔍 Testing Different Confidence Thresholds")
    print("=" * 40)
    
    try:
        yolo_model = YOLO(YOLO_MODEL)
        
        # Create a test image
        test_image = create_test_person_image()
        
        confidence_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        for conf in confidence_levels:
            results = yolo_model(test_image, conf=conf, verbose=False)
            detections = 0
            for result in results:
                if result.boxes is not None:
                    detections += len(result.boxes)
            
            print(f"Confidence {conf:.1f}: {detections} detections")
            
    except Exception as e:
        print(f"Error testing confidence thresholds: {e}")

if __name__ == "__main__":
    print("Starting YOLO detection debug...")
    
    # Test 1: Check available classes
    test_yolo_classes()
    
    # Test 2: Test different confidence thresholds
    test_different_confidence_thresholds()
    
    # Test 3: Full detection debug
    success = debug_yolo_detection()
    
    if success:
        print("\n🎉 Debug completed successfully!")
    else:
        print("\n❌ Debug failed. Check the error messages above.") 