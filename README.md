# Simple Multi-Camera Motion Detection

A real-time multi-camera object tracking and motion detection system built with Python, OpenCV, and YOLO. This project supports both local USB cameras and IP webcams for flexible deployment scenarios.

## 🚀 Features

- **Multi-Camera Support**: Connect multiple USB cameras or IP webcams
- **Real-Time Object Detection**: Powered by YOLOv8 for accurate object detection
- **Object Tracking**: DeepSORT algorithm for persistent object tracking across frames
- **Cross-Camera Tracking**: Track objects as they move between camera views
- **Visualization**: Real-time visualization with position mapping and trajectory display
- **IP Webcam Integration**: Support for Android IP Webcam and other IP camera sources
- **Configurable Settings**: Easy camera configuration through GUI or JSON files
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 📋 Requirements

- **Python**: 3.8 or higher
- **Cameras**: USB cameras or IP webcams
- **Memory**: At least 4GB RAM (8GB recommended)
- **Storage**: 2GB free space for models and dependencies

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Asiyil-K-Alaswad/Simple-Multi-Camera-Motion-Detection.git
cd Simple-Multi-Camera-Motion-Detection
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download YOLO Models

The system will automatically download YOLO models on first run, or you can manually download them:

```bash
# Download YOLOv8n (smaller, faster)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Download YOLOv8s (larger, more accurate)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

## 🎯 Quick Start

### Option 1: Run with Local Cameras

1. **Connect your cameras** to your computer
2. **Run the main application**:
   ```bash
   python main.py
   ```
3. **Configure cameras** in the GUI if needed

### Option 2: Run with IP Webcams

1. **Set up IP Webcam** (see [IP Webcam Integration Guide](IPWEBCAM_INTEGRATION_GUIDE.md))
2. **Configure camera settings**:
   ```bash
   python camera_config_ui.py
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

### Option 3: Demo Mode (No Cameras Required)

Test the system without physical cameras:

```bash
python test_demo.py
```

## 📁 Project Structure

```
Simple-Multi-Camera-Motion-Detection/
├── main.py                    # Main application entry point
├── camera_manager.py          # Camera feed management and threading
├── object_tracker.py          # YOLO detection and DeepSORT tracking
├── visualizer.py             # Real-time visualization and GUI
├── config.py                 # Configuration settings
├── camera_config_ui.py       # Camera configuration GUI
├── launcher.py               # Application launcher
├── setup.py                  # Setup script
├── requirements.txt          # Python dependencies
├── camera_config.json        # Camera configuration (user-specific)
├── sample_camera_config.json # Example camera configuration
├── *.bat files              # Windows batch scripts
├── test_*.py                # Test and demo scripts
├── *.md files               # Documentation
└── README.md                # This file
```

## ⚙️ Configuration

### Camera Configuration

Edit `camera_config.json` or use the GUI:

```json
{
  "cameras": [
    {
      "name": "Camera 1",
      "type": "usb",
      "index": 0,
      "resolution": [640, 480],
      "fps": 30
    },
    {
      "name": "IP Camera",
      "type": "ip",
      "url": "http://192.168.1.100:8080/video",
      "resolution": [640, 480],
      "fps": 30
    }
  ]
}
```

### Application Settings

Modify `config.py` for:
- Detection confidence thresholds
- Tracking parameters
- Visualization settings
- Performance options

## 🔧 Troubleshooting

### Common Issues

**Camera not detected:**
- Check device manager for camera availability
- Try different camera indices (0, 1, 2, etc.)
- Ensure camera is not being used by another application

**Performance issues:**
- Reduce frame resolution in camera configuration
- Use YOLOv8n instead of YOLOv8s
- Close other applications to free up resources

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility

**IP Webcam connection issues:**
- Verify IP address and port in camera configuration
- Check network connectivity
- Ensure IP Webcam app is running on device

### Getting Help

1. Check the documentation files in the project
2. Review test scripts for examples
3. Check the logs for error messages
4. Ensure all dependencies are properly installed

## 📚 Documentation

- [Camera Configuration Guide](CAMERA_CONFIGURATION_GUIDE.md)
- [IP Webcam Integration Guide](IPWEBCAM_INTEGRATION_GUIDE.md)
- [YOLO Configuration Guide](YOLO_CONFIGURATION_GUIDE.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- [Batch Files README](BATCH_FILES_README.md)

## 🧪 Testing

Run various test scripts to verify functionality:

```bash
# Test camera detection
python test_camera_frames.py

# Test IP webcam connection
python test_ip_webcam.py

# Test object tracking
python test_tracking_local.py

# Test YOLO detection
python test_yolo_deepsort.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [DeepSORT](https://github.com/mikel-brostrom/yolov8_tracking)
- [OpenCV](https://opencv.org/)
- [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam)

---

**Note**: This project requires cameras or IP webcams to function. For testing without hardware, use the demo mode. 