"""
Test script to demonstrate different YOLO class configurations
"""

import cv2
import numpy as np
import time
from ultralytics import YOLO
from config import *

def test_class_configurations():
    """Test different class configurations."""
    
    print("🧪 Testing Different YOLO Class Configurations")
    print("=" * 60)
    
    # Load YOLO model
    yolo_model = YOLO(YOLO_MODEL)
    print(f"Model: {YOLO_MODEL}")
    print(f"Available classes: {len(yolo_model.names)}")
    
    # Create a test image with various objects
    test_image = create_test_image()
    
    # Test different configurations
    configurations = [
        {
            'name': 'People Only',
            'classes': ['person'],
            'min_size': 1000,
            'max_size': 100000,
            'conf': 0.3
        },
        {
            'name': 'Vehicles',
            'classes': ['car', 'truck', 'bus', 'bicycle'],
            'min_size': 500,
            'max_size': 80000,
            'conf': 0.4
        },
        {
            'name': 'Indoor Objects',
            'classes': ['person', 'chair', 'tv', 'laptop'],
            'min_size': 200,
            'max_size': 50000,
            'conf': 0.3
        },
        {
            'name': 'All Classes (Debug)',
            'classes': [],  # Empty = all classes
            'min_size': 100,
            'max_size': 100000,
            'conf': 0.2
        }
    ]
    
    for config in configurations:
        print(f"\n🔧 Testing: {config['name']}")
        print("-" * 40)
        
        # Run detection with this configuration
        results = yolo_model(test_image, conf=config['conf'], verbose=False)
        
        detected_objects = []
        total_detections = 0
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                total_detections += len(boxes)
                for box in boxes:
                    # Get detection info
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = yolo_model.names[class_id]
                    
                    # Apply class filtering
                    if config['classes'] and class_name not in config['classes']:
                        continue
                    
                    # Apply size filtering
                    area = w * h
                    if area < config['min_size'] or area > config['max_size']:
                        continue
                    
                    detected_objects.append({
                        'class': class_name,
                        'confidence': confidence,
                        'area': area,
                        'bbox': (x, y, w, h)
                    })
        
        print(f"Total YOLO detections: {total_detections}")
        print(f"After filtering: {len(detected_objects)} objects")
        
        for obj in detected_objects:
            print(f"  ✓ {obj['class']} (conf: {obj['confidence']:.2f}, area: {obj['area']})")
    
    print("\n" + "=" * 60)
    print("📊 Configuration Summary")
    print("=" * 60)
    print("To use these configurations, edit config.py:")
    print()
    print("1. For people detection:")
    print("   TRACK_CLASSES = ['person']")
    print("   MIN_OBJECT_SIZE = 1000")
    print("   MAX_OBJECT_SIZE = 100000")
    print()
    print("2. For vehicle detection:")
    print("   TRACK_CLASSES = ['car', 'truck', 'bus', 'bicycle']")
    print("   MIN_OBJECT_SIZE = 500")
    print("   MAX_OBJECT_SIZE = 80000")
    print()
    print("3. For indoor monitoring:")
    print("   TRACK_CLASSES = ['person', 'chair', 'tv', 'laptop']")
    print("   MIN_OBJECT_SIZE = 200")
    print("   MAX_OBJECT_SIZE = 50000")
    print()
    print("4. For debugging (all objects):")
    print("   TRACK_CLASSES = []")
    print("   MIN_OBJECT_SIZE = 100")
    print("   MAX_OBJECT_SIZE = 100000")

def create_test_image():
    """Create a test image with various objects."""
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Background
    image[:] = (50, 50, 50)
    
    # Add various objects
    # Person-like shape
    cv2.rectangle(image, (200, 150), (260, 350), (255, 255, 255), -1)
    cv2.circle(image, (230, 120), 30, (255, 255, 255), -1)
    
    # Car-like shape
    cv2.rectangle(image, (400, 300), (500, 350), (0, 0, 255), -1)
    cv2.rectangle(image, (420, 280), (480, 300), (0, 0, 255), -1)
    
    # Chair-like shape
    cv2.rectangle(image, (100, 200), (150, 250), (0, 255, 0), -1)
    cv2.rectangle(image, (100, 180), (150, 200), (0, 255, 0), -1)
    
    # TV-like shape
    cv2.rectangle(image, (300, 100), (380, 180), (255, 0, 0), -1)
    
    # Add some noise
    noise = np.random.randint(0, 30, image.shape, dtype=np.uint8)
    image = cv2.add(image, noise)
    
    return image

if __name__ == "__main__":
    test_class_configurations() 