# YOLO Configuration Guide

This guide explains how to configure YOLO to detect and track different types of objects.

## 🔍 **Current Issue Analysis**

Based on the debug output, the system is working correctly but objects are being filtered out due to:

1. **Class Filtering**: Only 'person' class is being tracked
2. **Size Filtering**: Object size limits are too restrictive

## 📋 **Available YOLO Classes**

YOLOv8 can detect 80 different object classes. Here are the most common ones:

### **People and Animals**
- `person` (class 0)
- `cat` (class 15)
- `dog` (class 16)
- `horse` (class 17)
- `sheep` (class 18)
- `cow` (class 19)
- `elephant` (class 20)
- `bear` (class 21)
- `zebra` (class 22)
- `giraffe` (class 23)

### **Vehicles**
- `bicycle` (class 1)
- `car` (class 2)
- `motorcycle` (class 3)
- `airplane` (class 4)
- `bus` (class 5)
- `train` (class 6)
- `truck` (class 7)
- `boat` (class 8)

### **Common Objects**
- `tv` (class 62)
- `laptop` (class 63)
- `cell phone` (class 67)
- `book` (class 73)
- `chair` (class 56)
- `couch` (class 57)
- `bed` (class 59)
- `dining table` (class 60)

## ⚙️ **Configuration Examples**

### **1. Track Only People**
```python
# In config.py
TRACK_CLASSES = ['person']
MIN_OBJECT_SIZE = 1000    # Minimum person size
MAX_OBJECT_SIZE = 100000  # Maximum person size
YOLO_CONF_THRESHOLD = 0.3 # Lower confidence for better detection
```

### **2. Track People and Vehicles**
```python
# In config.py
TRACK_CLASSES = ['person', 'car', 'bicycle', 'motorcycle']
MIN_OBJECT_SIZE = 500     # Smaller minimum for vehicles
MAX_OBJECT_SIZE = 100000  # Large maximum
YOLO_CONF_THRESHOLD = 0.4
```

### **3. Track All Moving Objects**
```python
# In config.py
TRACK_CLASSES = ['person', 'car', 'bicycle', 'motorcycle', 'bus', 'truck']
MIN_OBJECT_SIZE = 300
MAX_OBJECT_SIZE = 100000
YOLO_CONF_THRESHOLD = 0.3
```

### **4. Track Indoor Objects**
```python
# In config.py
TRACK_CLASSES = ['person', 'chair', 'couch', 'tv', 'laptop']
MIN_OBJECT_SIZE = 200
MAX_OBJECT_SIZE = 100000
YOLO_CONF_THRESHOLD = 0.3
```

### **5. Track Everything (Debug Mode)**
```python
# In config.py
TRACK_CLASSES = []  # Empty list = track all classes
MIN_OBJECT_SIZE = 100
MAX_OBJECT_SIZE = 100000
YOLO_CONF_THRESHOLD = 0.2
```

## 🔧 **How to Configure**

### **Step 1: Edit config.py**
```python
# YOLOv8 Configuration
YOLO_MODEL = 'yolov8n.pt'  # Model size
YOLO_CONF_THRESHOLD = 0.3  # Detection confidence (0.1-1.0)
YOLO_IOU_THRESHOLD = 0.45  # IoU threshold
TRACK_CLASSES = ['person']  # Classes to track

# Object Detection Configuration
MIN_OBJECT_SIZE = 1000     # Minimum object size in pixels
MAX_OBJECT_SIZE = 100000   # Maximum object size in pixels
```

### **Step 2: Choose Object Classes**
Add the classes you want to track to the `TRACK_CLASSES` list:

```python
# Examples:
TRACK_CLASSES = ['person']                    # Only people
TRACK_CLASSES = ['person', 'car']             # People and cars
TRACK_CLASSES = ['person', 'car', 'bicycle']  # People, cars, and bicycles
TRACK_CLASSES = []                           # Track all classes (debug mode)
```

### **Step 3: Adjust Size Limits**
Set appropriate size limits for your objects:

```python
# For people (large objects)
MIN_OBJECT_SIZE = 1000
MAX_OBJECT_SIZE = 100000

# For vehicles (medium objects)
MIN_OBJECT_SIZE = 500
MAX_OBJECT_SIZE = 50000

# For small objects
MIN_OBJECT_SIZE = 100
MAX_OBJECT_SIZE = 10000
```

### **Step 4: Adjust Confidence Threshold**
```python
# Lower confidence = more detections (but more false positives)
YOLO_CONF_THRESHOLD = 0.2  # Very sensitive
YOLO_CONF_THRESHOLD = 0.3  # Balanced (recommended)
YOLO_CONF_THRESHOLD = 0.5  # More selective
YOLO_CONF_THRESHOLD = 0.7  # Very selective
```

## 🧪 **Testing Your Configuration**

### **1. Run the Debug Script**
```bash
python debug_yolo_detection.py
```

This will show you:
- What classes YOLO can detect
- What objects are being detected in your video
- What's being filtered out and why

### **2. Test Different Configurations**
```bash
# Test with different class lists
python demo_yolo_deepsort.py
```

### **3. Monitor the Logs**
The system now provides detailed logging:
- Raw detections from YOLO
- Filtering decisions
- Final accepted objects

## 📊 **Performance Tips**

### **Model Selection**
- `yolov8n.pt`: Fastest, good for real-time
- `yolov8s.pt`: Balanced speed/accuracy
- `yolov8m.pt`: Higher accuracy, slower
- `yolov8l.pt`: Maximum accuracy, slowest

### **Confidence vs Speed**
- Lower confidence = more detections = slower processing
- Higher confidence = fewer detections = faster processing

### **Class Selection**
- Fewer classes = faster processing
- More classes = more comprehensive detection

## 🐛 **Troubleshooting**

### **No Objects Detected**
1. Check if your target classes are in `TRACK_CLASSES`
2. Lower the `YOLO_CONF_THRESHOLD`
3. Increase `MAX_OBJECT_SIZE`
4. Run debug script to see raw detections

### **Too Many False Positives**
1. Increase `YOLO_CONF_THRESHOLD`
2. Reduce `TRACK_CLASSES` to only essential objects
3. Adjust size limits

### **Objects Too Small/Large**
1. Adjust `MIN_OBJECT_SIZE` and `MAX_OBJECT_SIZE`
2. Check the debug output for actual object sizes

### **Slow Performance**
1. Use smaller YOLO model (`yolov8n.pt`)
2. Reduce frame resolution
3. Increase `YOLO_CONF_THRESHOLD`
4. Reduce number of tracked classes

## 📝 **Example Configurations**

### **Surveillance System**
```python
TRACK_CLASSES = ['person', 'car', 'truck']
MIN_OBJECT_SIZE = 500
MAX_OBJECT_SIZE = 100000
YOLO_CONF_THRESHOLD = 0.4
```

### **Indoor Monitoring**
```python
TRACK_CLASSES = ['person', 'chair', 'tv', 'laptop']
MIN_OBJECT_SIZE = 200
MAX_OBJECT_SIZE = 50000
YOLO_CONF_THRESHOLD = 0.3
```

### **Traffic Monitoring**
```python
TRACK_CLASSES = ['car', 'truck', 'bus', 'motorcycle', 'bicycle']
MIN_OBJECT_SIZE = 300
MAX_OBJECT_SIZE = 80000
YOLO_CONF_THRESHOLD = 0.5
```

### **Wildlife Monitoring**
```python
TRACK_CLASSES = ['person', 'cat', 'dog', 'horse', 'cow', 'sheep']
MIN_OBJECT_SIZE = 100
MAX_OBJECT_SIZE = 100000
YOLO_CONF_THRESHOLD = 0.3
```

## 🎯 **Quick Start**

1. **For people detection**: Use the current configuration
2. **For vehicles**: Change `TRACK_CLASSES = ['car', 'truck', 'bus']`
3. **For everything**: Set `TRACK_CLASSES = []`
4. **For debugging**: Run `python debug_yolo_detection.py`

The system is now properly configured and should detect objects correctly! 