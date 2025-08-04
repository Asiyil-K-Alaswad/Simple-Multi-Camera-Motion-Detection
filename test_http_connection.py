#!/usr/bin/env python3
"""
Test script to verify HTTP connection to IP webcam.
This script tests the connection without using OpenCV to isolate the issue.
"""

import urllib.request
import urllib.error
import cv2
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_http_connectivity():
    """Test basic HTTP connectivity to the IP webcam."""
    
    test_urls = [
        "http://10.133.243.8:8080/shot.jpg",
        "http://10.133.243.8:8080/video",
        "http://10.133.243.8:8080/mjpeg",
    ]
    
    print("Testing HTTP connectivity...")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        try:
            # Test with urllib first (pure HTTP)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"✅ HTTP Status: {response.getcode()}")
                print(f"✅ Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
                print(f"✅ Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
                
                # Read a small amount of data to verify it's working
                data = response.read(1024)
                print(f"✅ Data received: {len(data)} bytes")
                
        except urllib.error.URLError as e:
            print(f"❌ HTTP Error: {e}")
        except Exception as e:
            print(f"❌ General Error: {e}")

def test_opencv_connection():
    """Test OpenCV connection with different backends."""
    
    test_urls = [
        "http://10.133.243.8:8080/shot.jpg",
        "http://10.133.243.8:8080/video",
    ]
    
    print("\n\nTesting OpenCV connection...")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting OpenCV with: {url}")
        
        # Test with FFMPEG backend
        try:
            print("  Trying FFMPEG backend...")
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"  ✅ FFMPEG Success - Frame shape: {frame.shape}")
                else:
                    print("  ❌ FFMPEG opened but failed to read frame")
                cap.release()
            else:
                print("  ❌ FFMPEG failed to open")
        except Exception as e:
            print(f"  ❌ FFMPEG Error: {e}")
        
        # Test with default backend
        try:
            print("  Trying default backend...")
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"  ✅ Default Success - Frame shape: {frame.shape}")
                else:
                    print("  ❌ Default opened but failed to read frame")
                cap.release()
            else:
                print("  ❌ Default failed to open")
        except Exception as e:
            print(f"  ❌ Default Error: {e}")

def test_network_connectivity():
    """Test basic network connectivity."""
    
    print("\n\nTesting network connectivity...")
    print("=" * 50)
    
    import socket
    
    try:
        # Test TCP connection to the IP and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('10.133.243.8', 8080))
        if result == 0:
            print("✅ TCP connection to 10.133.243.8:8080 successful")
        else:
            print(f"❌ TCP connection to 10.133.243.8:8080 failed with error code: {result}")
        sock.close()
    except Exception as e:
        print(f"❌ Network test error: {e}")

if __name__ == "__main__":
    print("IP Webcam HTTP Connection Test")
    print("=" * 50)
    
    # Test network connectivity first
    test_network_connectivity()
    
    # Test HTTP connectivity
    test_http_connectivity()
    
    # Test OpenCV connection
    test_opencv_connection()
    
    print("\n\nTesting completed!") 