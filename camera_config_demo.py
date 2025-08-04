"""
Camera Configuration Demo

Demonstrates the camera configuration interface features.
"""

import cv2
import json
import os
from config import *

def demo_camera_configuration():
    """Demonstrate camera configuration features."""
    
    print("📹 Camera Configuration Demo")
    print("=" * 50)
    print("This demo shows the camera configuration interface features.")
    print()
    
    # Show available camera devices
    print("🔍 Available Camera Devices:")
    devices = get_available_devices()
    if devices:
        for device in devices:
            print(f"  ✓ Device {device}")
    else:
        print("  ⚠ No camera devices found")
    print()
    
    # Show example configurations
    print("⚙️ Example Camera Configurations:")
    print()
    
    examples = [
        {
            'name': 'USB Webcams',
            'camera1': {'type': 'device', 'device_index': 0, 'name': 'Front Camera'},
            'camera2': {'type': 'device', 'device_index': 1, 'name': 'Side Camera'}
        },
        {
            'name': 'IP Cameras',
            'camera1': {'type': 'url', 'url': 'rtsp://192.168.1.100:554/stream1', 'name': 'IP Camera 1'},
            'camera2': {'type': 'url', 'url': 'rtsp://192.168.1.101:554/stream1', 'name': 'IP Camera 2'}
        },
        {
            'name': 'Video Files',
            'camera1': {'type': 'url', 'url': 'file:///path/to/video1.mp4', 'name': 'Video 1'},
            'camera2': {'type': 'url', 'url': 'file:///path/to/video2.mp4', 'name': 'Video 2'}
        },
        {
            'name': 'Mixed Setup',
            'camera1': {'type': 'device', 'device_index': 0, 'name': 'Live Camera'},
            'camera2': {'type': 'url', 'url': 'rtsp://192.168.1.100:554/stream1', 'name': 'IP Camera'}
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}:")
        print(f"   Camera 1: {example['camera1']['type']} - {example['camera1']['name']}")
        print(f"   Camera 2: {example['camera2']['type']} - {example['camera2']['name']}")
        print()
    
    # Show configuration file format
    print("📄 Configuration File Format (camera_config.json):")
    print()
    config_example = {
        "camera1": {
            "type": "device",
            "device_index": 0,
            "url": "",
            "name": "Camera 1",
            "enabled": True
        },
        "camera2": {
            "type": "url",
            "device_index": 1,
            "url": "rtsp://192.168.1.100:554/stream1",
            "name": "IP Camera",
            "enabled": True
        }
    }
    
    print(json.dumps(config_example, indent=2))
    print()
    
    # Show usage instructions
    print("🚀 How to Use:")
    print()
    print("1. Start the launcher:")
    print("   python launcher.py")
    print()
    print("2. Configure cameras in the GUI:")
    print("   - Select camera type (device/url)")
    print("   - Choose device index or enter URL")
    print("   - Set camera names")
    print("   - Enable/disable cameras")
    print()
    print("3. Test camera connections:")
    print("   - Click 'Test Cameras' to see live previews")
    print("   - Verify both cameras are working")
    print()
    print("4. Save and start:")
    print("   - Click 'Save Configuration'")
    print("   - Click 'Start Application'")
    print()
    
    # Show quick start option
    print("⚡ Quick Start (skip configuration):")
    print("   python launcher.py --quick")
    print()

def get_available_devices():
    """Get list of available camera devices."""
    devices = []
    for i in range(10):  # Check first 10 devices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            devices.append(str(i))
            cap.release()
    return devices

def show_supported_urls():
    """Show supported URL formats."""
    print("🌐 Supported URL Formats:")
    print()
    
    url_examples = [
        ("RTSP Stream", "rtsp://192.168.1.100:554/stream1"),
        ("HTTP Stream", "http://192.168.1.100:8080/video"),
        ("Video File", "file:///path/to/video.mp4"),
        ("YouTube (if supported)", "https://www.youtube.com/watch?v=VIDEO_ID"),
        ("IP Camera", "rtsp://username:password@192.168.1.100:554/stream1")
    ]
    
    for name, url in url_examples:
        print(f"  {name}: {url}")
    print()

def show_troubleshooting():
    """Show troubleshooting tips."""
    print("🔧 Troubleshooting Tips:")
    print()
    
    tips = [
        "Camera not detected: Check USB connection and drivers",
        "RTSP stream not working: Verify network connectivity and credentials",
        "Video file not playing: Check file path and format support",
        "Low FPS: Reduce frame resolution or use smaller YOLO model",
        "High CPU usage: Disable one camera or use smaller frame size"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

def create_sample_config():
    """Create a sample configuration file."""
    sample_config = {
        "camera1": {
            "type": "device",
            "device_index": 0,
            "url": "",
            "name": "USB Camera",
            "enabled": True
        },
        "camera2": {
            "type": "device",
            "device_index": 1,
            "url": "",
            "name": "Secondary Camera",
            "enabled": True
        }
    }
    
    try:
        with open('sample_camera_config.json', 'w') as f:
            json.dump(sample_config, f, indent=2)
        print("✅ Sample configuration file created: sample_camera_config.json")
    except Exception as e:
        print(f"❌ Error creating sample config: {e}")

if __name__ == "__main__":
    demo_camera_configuration()
    show_supported_urls()
    show_troubleshooting()
    create_sample_config()
    
    print("🎉 Camera configuration demo completed!")
    print("\nTo start the camera configuration interface:")
    print("python launcher.py") 