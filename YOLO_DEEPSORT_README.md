# YOLOv8 + DeepSORT Integration

This document describes the integration of YOLOv8 object detection with DeepSORT tracking in the multi-camera object tracking system.

## Overview

The object tracker has been upgraded from simple motion detection to use:
- **YOLOv8**: State-of-the-art object detection model
- **DeepSORT**: Advanced multi-object tracking algorithm

## Key Features

### YOLOv8 Detection
- Uses pre-trained YOLOv8 models (nano, small, medium, large, xlarge)
- Configurable confidence and IoU thresholds
- Supports multiple object classes (person, car, etc.)
- Automatic model download on first run

### DeepSORT Tracking
- Maintains consistent track IDs across frames
- Handles object occlusion and re-identification
- Uses deep learning embeddings for robust tracking
- Configurable tracking parameters

### Multi-Camera Support
- Separate DeepSORT trackers for each camera
- 3D position calculation using stereo vision
- Cross-camera object matching

## Configuration

### YOLOv8 Settings (config.py)
```python
# YOLOv8 Configuration
YOLO_MODEL = 'yolov8n.pt'  # Model size: n(nano), s(small), m(medium), l(large), x(xlarge)
YOLO_IOU_THRESHOLD = 0.45
YOLO_CONF_THRESHOLD = 0.5
TRACK_CLASSES = ['person']  # Classes to track
```

### DeepSORT Settings (config.py)
```python
# DeepSORT Configuration
DEEPSORT_MAX_AGE = 30
DEEPSORT_N_INIT = 3
DEEPSORT_NMS_MAX_OVERLAP = 1.0
DEEPSORT_MAX_COSINE_DISTANCE = 0.2
DEEPSORT_EMBEDDER = "mobilenet"
DEEPSORT_HALF = True
DEEPSORT_BGR = True
DEEPSORT_EMBEDDER_GPU = True
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The system will automatically download the YOLOv8 model on first run.

## Usage

### Basic Usage
```python
from object_tracker import ObjectTracker

# Initialize tracker
tracker = ObjectTracker()

# Track objects in frames
tracked_objects = tracker.track_objects(frame1, frame2)

# Draw detections
frame_with_detections = tracker.draw_detections(frame, tracked_objects["camera1"])
```

### Testing
Run the test script to verify the integration:
```bash
python test_yolo_deepsort.py
```

## Model Performance

### YOLOv8 Model Comparison
| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| yolov8n.pt | 6.3MB | Fastest | Good | Real-time applications |
| yolov8s.pt | 22.6MB | Fast | Better | Balanced performance |
| yolov8m.pt | 52.2MB | Medium | High | High accuracy needed |
| yolov8l.pt | 87.7MB | Slow | Higher | Maximum accuracy |
| yolov8x.pt | 136.6MB | Slowest | Highest | Research/offline |

### Recommended Settings
- **Real-time**: Use `yolov8n.pt` with `TRACK_CLASSES = ['person']`
- **High accuracy**: Use `yolov8s.pt` or `yolov8m.pt`
- **Multiple classes**: Add more classes to `TRACK_CLASSES`

## Tracking Information

Each tracked object contains:
- **Track ID**: Unique identifier maintained across frames
- **Bounding Box**: (x, y, width, height) coordinates
- **Class**: Object class (person, car, etc.)
- **Confidence**: Detection confidence score
- **3D Position**: Calculated using stereo vision (if available)

## Visualization

The system draws:
- Bounding boxes around detected objects
- Track IDs and class names
- Confidence scores
- 3D positions (when available)

## Troubleshooting

### Common Issues

1. **Slow Performance**
   - Use smaller YOLOv8 model (`yolov8n.pt`)
   - Reduce frame resolution
   - Enable GPU acceleration if available

2. **Poor Detection**
   - Increase `YOLO_CONF_THRESHOLD`
   - Use larger YOLOv8 model
   - Check lighting conditions

3. **Tracking Issues**
   - Adjust `DEEPSORT_MAX_AGE`
   - Modify `DEEPSORT_MAX_COSINE_DISTANCE`
   - Check camera synchronization

### GPU Acceleration
To enable GPU acceleration:
1. Install CUDA-compatible PyTorch
2. Set `DEEPSORT_EMBEDDER_GPU = True`
3. Ensure CUDA is available

## Performance Tips

1. **Model Selection**: Choose the right YOLOv8 model for your use case
2. **Frame Rate**: Balance between accuracy and speed
3. **Resolution**: Lower resolution = faster processing
4. **GPU**: Use GPU acceleration when available
5. **Filtering**: Only track necessary object classes

## Future Enhancements

- Custom YOLOv8 model training
- Additional tracking algorithms
- Advanced 3D reconstruction
- Multi-class tracking optimization
- Real-time performance monitoring 