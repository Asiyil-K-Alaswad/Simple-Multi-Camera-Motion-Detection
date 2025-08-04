"""
Configuration settings for the multi-camera object tracking system.
"""

# Camera Configuration
CAMERA_1_INDEX = 0  # First camera device index
CAMERA_2_INDEX = 1  # Second camera device index

# Frame Configuration
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# URL Camera Configuration (for IP webcams)
URL_CAMERA_BUFFER_SIZE = 1  # Reduce buffer size for MJPEG streams
URL_CAMERA_TIMEOUT = 5  # Timeout for URL camera operations
URL_CAMERA_RETRY_ATTEMPTS = 3  # Number of retry attempts for URL cameras
CAMERA_THREAD_TIMEOUT = 2.0  # Timeout for camera thread operations

# Display Configuration
DISPLAY_WIDTH = 640   # Display window width (can be different from capture)
DISPLAY_HEIGHT = 480  # Display window height (can be different from capture)
DISPLAY_SCALE = 1.0   # Scale factor for display (1.0 = original size, 0.5 = half size, 2.0 = double size)

# Camera Placement (in meters)
CAMERA_DISTANCE = 0.5  # Distance between cameras
CAMERA_HEIGHT = 1.0    # Height of cameras from ground

# Object Detection Configuration
DETECTION_THRESHOLD = 0.5
MIN_OBJECT_SIZE = 500    # Minimum object size in pixels (reduced for better detection)
MAX_OBJECT_SIZE = 200000  # Maximum object size in pixels (increased for better detection)

# YOLOv8 Configuration
YOLO_MODEL = 'yolov8s.pt'  # Model size: n(nano), s(small), m(medium), l(large), x(xlarge)
YOLO_IOU_THRESHOLD = 0.45
YOLO_CONF_THRESHOLD = 0.3  # Increased for better quality detections
TRACK_CLASSES = ["car"]  # Common objects to track

# Common YOLO classes you might want to track:
# YOLO_CLASSES = {
#     'person': 0,
#     'bicycle': 1,
#     'car': 2,
#     'motorcycle': 3,
#     'airplane': 4,
#     'bus': 5,
#     'train': 6,
#     'truck': 7,
#     'boat': 8,
#     'traffic light': 9,
#     'fire hydrant': 10,
#     'stop sign': 11,
#     'parking meter': 12,
#     'bench': 13,
#     'bird': 14,
#     'cat': 15,
#     'dog': 16,
#     'horse': 17,
#     'sheep': 18,
#     'cow': 19,
#     'elephant': 20,
#     'bear': 21,
#     'zebra': 22,
#     'giraffe': 23,
#     'backpack': 24,
#     'umbrella': 25,
#     'handbag': 26,
#     'tie': 27,
#     'suitcase': 28,
#     'frisbee': 29,
#     'skis': 30,
#     'snowboard': 31,
#     'sports ball': 32,
#     'kite': 33,
#     'baseball bat': 34,
#     'baseball glove': 35,
#     'skateboard': 36,
#     'surfboard': 37,
#     'tennis racket': 38,
#     'bottle': 39,
#     'wine glass': 40,
#     'cup': 41,
#     'fork': 42,
#     'knife': 43,
#     'spoon': 44,
#     'bowl': 45,
#     'banana': 46,
#     'apple': 47,
#     'sandwich': 48,
#     'orange': 49,
#     'broccoli': 50,
#     'carrot': 51,
#     'hot dog': 52,
#     'pizza': 53,
#     'donut': 54,
#     'cake': 55,
#     'chair': 56,
#     'couch': 57,
#     'potted plant': 58,
#     'bed': 59,
#     'dining table': 60,
#     'toilet': 61,
#     'tv': 62,
#     'laptop': 63,
#     'mouse': 64,
#     'remote': 65,
#     'keyboard': 66,
#     'cell phone': 67,
#     'microwave': 68,
#     'oven': 69,
#     'toaster': 70,
#     'sink': 71,
#     'refrigerator': 72,
#     'book': 73,
#     'clock': 74,
#     'vase': 75,
#     'scissors': 76,
#     'teddy bear': 77,
#     'hair drier': 78,
#     'toothbrush': 79
# }

# DeepSORT Configuration
DEEPSORT_MAX_AGE = 30
DEEPSORT_N_INIT = 3
DEEPSORT_NMS_MAX_OVERLAP = 1.0
DEEPSORT_MAX_COSINE_DISTANCE = 0.2
DEEPSORT_EMBEDDER = "mobilenet"
DEEPSORT_HALF = True
DEEPSORT_BGR = True
DEEPSORT_EMBEDDER_GPU = True

# Tracking Configuration
TRACKING_HISTORY_LENGTH = 30  # Number of frames to keep tracking history
TRACKING_THRESHOLD = 0.7      # Confidence threshold for tracking

# Visualization Configuration
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
UPDATE_RATE = 30  # Hz

# Threading Configuration
CAMERA_THREAD_TIMEOUT = 1.0  # seconds
PROCESSING_THREAD_TIMEOUT = 0.1  # seconds

# Debug Configuration
DEBUG_MODE = True
SAVE_FRAMES = False
LOG_LEVEL = "INFO" 