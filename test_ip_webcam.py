#!/usr/bin/env python3
"""
Test script for IP webcam URL formatting and connectivity.
"""

import cv2
import time
import logging
from camera_manager import CameraStream

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_url_formatting():
    """Test URL formatting for different IP webcam formats."""
    
    test_urls = [
        "10.133.243.8:8080/video",  # Current config
        "192.168.1.100:8080/video",
        "192.168.1.100:8080/shot.jpg",
        "192.168.1.100:8080/mjpeg",
        "rtsp://192.168.1.100:8080/stream",
        "http://192.168.1.100:8080/videofeed",
    ]
    
    print("Testing URL formatting...")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nOriginal URL: {url}")
        
        # Create a temporary camera stream to test formatting
        temp_camera = CameraStream(url, "Test", "url")
        formatted_url = temp_camera._format_ip_webcam_url(url)
        print(f"Formatted URL: {formatted_url}")
        
        # Test connectivity
        try:
            cap = cv2.VideoCapture(formatted_url)
            if cap.isOpened():
                print("✅ URL is accessible")
                cap.release()
            else:
                print("❌ URL is not accessible")
        except Exception as e:
            print(f"❌ Error testing URL: {e}")

def test_current_config():
    """Test the current camera configuration."""
    
    print("\n\nTesting current camera configuration...")
    print("=" * 50)
    
    # Test camera2 (IP webcam)
    try:
        camera = CameraStream("10.133.243.8:8080/video", "IP Webcam Test", "url")
        print(f"Testing IP webcam: 10.133.243.8:8080/video")
        
        if camera.start():
            print("✅ IP webcam started successfully")
            
            # Try to read a few frames
            for i in range(5):
                frame = camera.get_frame()
                if frame is not None:
                    print(f"✅ Frame {i+1} received - Shape: {frame.shape}")
                else:
                    print(f"❌ Frame {i+1} failed")
                time.sleep(0.5)
            
            camera.stop()
            print("✅ IP webcam test completed")
        else:
            print("❌ Failed to start IP webcam")
            
    except Exception as e:
        print(f"❌ Error testing IP webcam: {e}")

def test_alternative_urls():
    """Test alternative URL formats for the same IP."""
    
    print("\n\nTesting alternative URL formats...")
    print("=" * 50)
    
    base_ip = "10.133.243.8:8080"
    alternative_urls = [
        f"http://{base_ip}/video",
        f"http://{base_ip}/shot.jpg",
        f"http://{base_ip}/mjpeg",
        f"http://{base_ip}/videofeed",
        f"http://{base_ip}/stream",
    ]
    
    for url in alternative_urls:
        print(f"\nTesting: {url}")
        try:
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"✅ Success - Frame shape: {frame.shape}")
                else:
                    print("❌ Failed to read frame")
                cap.release()
            else:
                print("❌ Failed to open URL")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("IP Webcam URL Testing Tool")
    print("=" * 50)
    
    # Test URL formatting
    test_url_formatting()
    
    # Test current configuration
    test_current_config()
    
    # Test alternative URLs
    test_alternative_urls()
    
    print("\n\nTesting completed!") 