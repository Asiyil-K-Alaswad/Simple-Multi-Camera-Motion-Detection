# Camera Configuration Guide

## 🎯 **Overview**

The camera configuration interface allows you to configure camera devices and URLs before starting the multi-camera object tracking application. This provides flexibility to use different types of camera sources including USB webcams, IP cameras, RTSP streams, and video files.

## ✅ **Features**

### **Camera Types Supported**
- **Device Cameras**: USB webcams, built-in cameras
- **URL Cameras**: RTSP streams, HTTP streams, video files
- **Mixed Setup**: Combine device and URL cameras

### **Configuration Options**
- Camera enable/disable
- Custom camera names
- Device index selection
- URL input with file browser
- Live camera testing and preview
- Configuration save/load

### **User Interface**
- Intuitive GUI with real-time previews
- Camera testing functionality
- Configuration validation
- Error handling and feedback

## 🚀 **Quick Start**

### **Method 1: Interactive Configuration**
```bash
python launcher.py
```

### **Method 2: Quick Start (Default Settings)**
```bash
python launcher.py --quick
```

### **Method 3: Direct Application Start**
```bash
python main.py
```

## 📋 **Step-by-Step Configuration**

### **1. Launch Configuration Interface**
```bash
python launcher.py
```

### **2. Configure Camera 1**
- **Enable Camera**: Check to enable Camera 1
- **Name**: Enter a descriptive name (e.g., "Front Camera")
- **Type**: Choose between "device" or "url"
- **Device**: Select device index (0, 1, 2, etc.)
- **URL**: Enter camera URL (for URL type)

### **3. Configure Camera 2**
- **Enable Camera**: Check to enable Camera 2
- **Name**: Enter a descriptive name (e.g., "Side Camera")
- **Type**: Choose between "device" or "url"
- **Device**: Select device index (0, 1, 2, etc.)
- **URL**: Enter camera URL (for URL type)

### **4. Test Cameras**
- Click **"Test Cameras"** to see live previews
- Verify both cameras are working correctly
- Check preview quality and frame rate

### **5. Save Configuration**
- Click **"Save Configuration"** to save settings
- Configuration is saved to `camera_config.json`

### **6. Start Application**
- Click **"Start Application"** to launch the main application
- The application will use your configured camera settings

## 📄 **Configuration File Format**

The camera configuration is stored in `camera_config.json`:

```json
{
  "camera1": {
    "type": "device",
    "device_index": 0,
    "url": "",
    "name": "Front Camera",
    "enabled": true
  },
  "camera2": {
    "type": "url",
    "device_index": 1,
    "url": "rtsp://192.168.1.100:554/stream1",
    "name": "IP Camera",
    "enabled": true
  }
}
```

### **Configuration Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | "device" for USB cameras, "url" for streams/files |
| `device_index` | integer | Camera device index (0, 1, 2, etc.) |
| `url` | string | Camera URL or file path |
| `name` | string | Custom camera name |
| `enabled` | boolean | Enable/disable camera |

## 🌐 **Supported URL Formats**

### **RTSP Streams**
```
rtsp://192.168.1.100:554/stream1
rtsp://username:password@192.168.1.100:554/stream1
rtsp://192.168.1.100:554/h264Preview_01_main
```

### **HTTP Streams**
```
http://192.168.1.100:8080/video
http://192.168.1.100:8080/stream.mjpeg
```

### **Video Files**
```
file:///path/to/video.mp4
file:///path/to/video.avi
file:///path/to/video.mov
```

### **IP Camera Examples**
```
rtsp://admin:password@192.168.1.100:554/stream1
rtsp://192.168.1.100:554/h264Preview_01_main
http://192.168.1.100:8080/video
```

## ⚙️ **Example Configurations**

### **USB Webcams**
```json
{
  "camera1": {
    "type": "device",
    "device_index": 0,
    "url": "",
    "name": "Front Camera",
    "enabled": true
  },
  "camera2": {
    "type": "device",
    "device_index": 1,
    "url": "",
    "name": "Side Camera",
    "enabled": true
  }
}
```

### **IP Cameras**
```json
{
  "camera1": {
    "type": "url",
    "device_index": 0,
    "url": "rtsp://192.168.1.100:554/stream1",
    "name": "IP Camera 1",
    "enabled": true
  },
  "camera2": {
    "type": "url",
    "device_index": 1,
    "url": "rtsp://192.168.1.101:554/stream1",
    "name": "IP Camera 2",
    "enabled": true
  }
}
```

### **Video Files**
```json
{
  "camera1": {
    "type": "url",
    "device_index": 0,
    "url": "file:///path/to/video1.mp4",
    "name": "Video 1",
    "enabled": true
  },
  "camera2": {
    "type": "url",
    "device_index": 1,
    "url": "file:///path/to/video2.mp4",
    "name": "Video 2",
    "enabled": true
  }
}
```

### **Mixed Setup**
```json
{
  "camera1": {
    "type": "device",
    "device_index": 0,
    "url": "",
    "name": "Live Camera",
    "enabled": true
  },
  "camera2": {
    "type": "url",
    "device_index": 1,
    "url": "rtsp://192.168.1.100:554/stream1",
    "name": "IP Camera",
    "enabled": true
  }
}
```

### **Single Camera Setup**
```json
{
  "camera1": {
    "type": "device",
    "device_index": 0,
    "url": "",
    "name": "Main Camera",
    "enabled": true
  },
  "camera2": {
    "type": "device",
    "device_index": 1,
    "url": "",
    "name": "Secondary Camera",
    "enabled": false
  }
}
```

## 🔧 **Troubleshooting**

### **Camera Not Detected**
1. **Check USB Connection**: Ensure camera is properly connected
2. **Install Drivers**: Install appropriate camera drivers
3. **Test with Other Software**: Verify camera works with other applications
4. **Check Device Index**: Try different device indices (0, 1, 2, etc.)

### **RTSP Stream Not Working**
1. **Network Connectivity**: Verify network connection to camera
2. **Credentials**: Check username/password in URL
3. **Port Access**: Ensure firewall allows RTSP traffic (port 554)
4. **Stream URL**: Verify correct stream URL format
5. **Test with VLC**: Try opening stream in VLC media player

### **Video File Not Playing**
1. **File Path**: Check file path is correct and accessible
2. **File Format**: Ensure file format is supported (MP4, AVI, MOV)
3. **File Permissions**: Verify read permissions for the file
4. **Codec Support**: Ensure video codec is supported by OpenCV

### **Low Performance**
1. **Reduce Frame Size**: Use smaller frame resolution
2. **Use Smaller YOLO Model**: Switch to `yolov8n.pt` for faster processing
3. **Disable One Camera**: Run with single camera for testing
4. **Check CPU Usage**: Monitor system resources

### **High CPU Usage**
1. **Reduce Frame Rate**: Lower FPS in configuration
2. **Use Smaller Model**: Switch to nano or small YOLO model
3. **Optimize Frame Size**: Use smaller frame dimensions
4. **Disable Features**: Turn off unnecessary features

## 📊 **Performance Tips**

### **For Real-time Applications**
- Use device cameras instead of network streams
- Set frame size to 640x480 or smaller
- Use `yolov8n.pt` model for fastest processing
- Enable only necessary cameras

### **For High Quality**
- Use larger frame sizes (1280x720 or higher)
- Use `yolov8s.pt` or `yolov8m.pt` models
- Ensure good lighting conditions
- Use high-quality camera hardware

### **For Network Cameras**
- Use wired network connection
- Ensure sufficient bandwidth
- Use appropriate RTSP URL format
- Consider using HTTP streams for better compatibility

## 🎮 **Advanced Configuration**

### **Manual Configuration File Editing**
You can manually edit `camera_config.json` for advanced configurations:

```json
{
  "camera1": {
    "type": "url",
    "device_index": 0,
    "url": "rtsp://admin:password@192.168.1.100:554/stream1",
    "name": "Security Camera 1",
    "enabled": true
  },
  "camera2": {
    "type": "url",
    "device_index": 1,
    "url": "file:///C:/Videos/sample.mp4",
    "name": "Test Video",
    "enabled": true
  }
}
```

### **Multiple Configuration Files**
You can create multiple configuration files for different setups:

```bash
# Create different configurations
cp camera_config.json usb_cameras.json
cp camera_config.json ip_cameras.json
cp camera_config.json video_files.json

# Load specific configuration
python launcher.py --config ip_cameras.json
```

## 📝 **Command Line Options**

### **Launcher Options**
```bash
python launcher.py              # Start with camera configuration
python launcher.py --quick      # Quick start with defaults
python launcher.py --help       # Show help information
```

### **Direct Application Start**
```bash
python main.py                  # Start with existing configuration
python demo_yolo_deepsort.py    # Start demo with webcam
```

## 🔍 **Testing and Validation**

### **Camera Testing**
1. **Test Cameras Button**: Use the "Test Cameras" button in the GUI
2. **Preview Windows**: Check live previews for both cameras
3. **Frame Rate**: Monitor FPS display for performance
4. **Quality Check**: Verify image quality and resolution

### **Configuration Validation**
1. **Save Configuration**: Always save after making changes
2. **Load Configuration**: Test loading saved configurations
3. **Error Messages**: Check for error messages in the GUI
4. **Log Files**: Review log files for detailed error information

## 📚 **Additional Resources**

### **Demo Scripts**
- `camera_config_demo.py`: Demonstrates configuration features
- `demo_yolo_deepsort.py`: Shows YOLO + DeepSORT integration
- `test_frame_sizes.py`: Tests frame size configurations

### **Documentation**
- `FRAME_SIZE_FIX.md`: Frame size configuration guide
- `YOLO_CONFIGURATION_GUIDE.md`: YOLO detection configuration
- `IMPLEMENTATION_SUMMARY.md`: Complete system overview

### **Configuration Files**
- `camera_config.json`: Camera configuration
- `config.py`: Main application configuration
- `requirements.txt`: Python dependencies

## 🎉 **Success Indicators**

### **Configuration Success**
- ✅ Both cameras show live previews
- ✅ No error messages in GUI
- ✅ Configuration saves successfully
- ✅ Application starts without errors

### **Performance Success**
- ✅ FPS above 15 for real-time applications
- ✅ CPU usage below 80%
- ✅ No frame drops or lag
- ✅ Stable camera connections

## 🆘 **Getting Help**

### **Common Issues**
1. **Camera not detected**: Check device index and drivers
2. **RTSP stream issues**: Verify network and credentials
3. **Performance problems**: Reduce frame size or model complexity
4. **Configuration errors**: Check JSON syntax and file permissions

### **Support Resources**
- Check log files for detailed error information
- Use demo scripts to test individual components
- Review troubleshooting section above
- Verify camera compatibility with OpenCV

The camera configuration system provides a flexible and user-friendly way to set up different camera sources for the multi-camera object tracking application. With support for device cameras, network streams, and video files, you can configure the system for various use cases and requirements. 