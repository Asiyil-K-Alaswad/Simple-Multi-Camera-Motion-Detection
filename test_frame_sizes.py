"""
Test script for frame size configuration
"""

import cv2
import numpy as np
from config import *

def test_frame_sizes():
    """Test different frame sizes and display configurations."""
    
    print("🧪 Testing Frame Size Configuration")
    print("=" * 50)
    
    # Test different frame sizes
    test_sizes = [
        (320, 240, 0.5, "Small"),
        (640, 480, 1.0, "Medium"),
        (1280, 720, 1.5, "Large"),
        (1920, 1080, 2.0, "HD")
    ]
    
    for width, height, scale, name in test_sizes:
        print(f"\n📐 Testing {name} configuration:")
        print(f"  Frame size: {width}x{height}")
        print(f"  Display scale: {scale}")
        
        # Calculate display size
        display_width = int(width * scale)
        display_height = int(height * scale)
        print(f"  Display size: {display_width}x{display_height}")
        
        # Calculate window size
        window_width = max(800 + 400, display_width * 2 + 100)
        window_height = max(600 + 200, display_height + 300)
        print(f"  Window size: {window_width}x{window_height}")
        
        # Test if sizes are reasonable
        if display_width > 0 and display_height > 0:
            print(f"  ✓ Valid configuration")
        else:
            print(f"  ✗ Invalid configuration")
    
    print("\n" + "=" * 50)
    print("📋 Configuration Summary")
    print("=" * 50)
    print("To change frame sizes:")
    print("1. Edit config.py:")
    print("   FRAME_WIDTH = 640")
    print("   FRAME_HEIGHT = 480")
    print("   DISPLAY_SCALE = 1.0")
    print()
    print("2. Or use the GUI Settings menu:")
    print("   Settings → Frame Size Settings")
    print()
    print("3. Available presets:")
    print("   - Small (320x240) - 0.5x scale")
    print("   - Medium (640x480) - 1.0x scale")
    print("   - Large (1280x720) - 1.5x scale")
    print("   - HD (1920x1080) - 2.0x scale")

def test_camera_frame_capture():
    """Test camera frame capture with different sizes."""
    
    print("\n📹 Testing Camera Frame Capture")
    print("=" * 40)
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No camera available for testing")
        return
    
    # Test different frame sizes
    test_sizes = [(320, 240), (640, 480), (1280, 720)]
    
    for width, height in test_sizes:
        print(f"\nTesting {width}x{height}:")
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Read frame
        ret, frame = cap.read()
        if ret:
            actual_width = frame.shape[1]
            actual_height = frame.shape[0]
            print(f"  Requested: {width}x{height}")
            print(f"  Actual: {actual_width}x{actual_height}")
            
            if actual_width == width and actual_height == height:
                print(f"  ✓ Size matches")
            else:
                print(f"  ⚠ Camera adjusted size")
        else:
            print(f"  ✗ Failed to capture frame")
    
    cap.release()

if __name__ == "__main__":
    test_frame_sizes()
    test_camera_frame_capture()
    print("\n🎉 Frame size testing completed!") 