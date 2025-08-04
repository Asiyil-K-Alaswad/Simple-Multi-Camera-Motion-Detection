"""
Object Tracker Module

Handles object detection using YOLOv8 and tracking using DeepSORT.
"""

import cv2
import numpy as np
import time
from typing import List, Tuple, Optional, Dict
import logging
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import *

logger = logging.getLogger(__name__)


class DetectedObject:
    """Represents a detected object with tracking information."""
    
    def __init__(self, bbox: Tuple[int, int, int, int], confidence: float, class_id: int, class_name: str, camera_id: str):
        """
        Initialize detected object.
        
        Args:
            bbox: Bounding box (x, y, width, height)
            confidence: Detection confidence
            class_id: YOLO class ID
            class_name: YOLO class name
            camera_id: ID of camera that detected the object
        """
        self.bbox = bbox
        self.confidence = confidence
        self.class_id = class_id
        self.class_name = class_name
        self.camera_id = camera_id
        self.timestamp = time.time()
        self.track_id = None
        self.position_3d = None
        
    def get_center(self) -> Tuple[int, int]:
        """Get center point of the bounding box."""
        x, y, w, h = self.bbox
        return (x + w // 2, y + h // 2)
    
    def get_area(self) -> int:
        """Get area of the bounding box."""
        x, y, w, h = self.bbox
        return w * h


class ObjectTracker:
    """Main object tracking system using YOLOv8 and DeepSORT."""
    
    def __init__(self):
        """Initialize object tracker."""
        self.tracked_objects = {}
        self.object_history = {}
        self.last_detection_time = {}
        
        # Initialize YOLOv8 detector
        self._initialize_yolo_detector()
        
        # Initialize DeepSORT trackers for each camera
        self._initialize_deepsort_trackers()
        
    def _initialize_yolo_detector(self):
        """Initialize the YOLOv8 object detection system."""
        try:
            # Load YOLOv8 model (will download automatically if not present)
            self.yolo_model = YOLO(YOLO_MODEL)
            
            # Set detection parameters
            self.conf_threshold = YOLO_CONF_THRESHOLD
            self.iou_threshold = YOLO_IOU_THRESHOLD
            
            logger.info(f"YOLOv8 detector initialized successfully with model: {YOLO_MODEL}")
            
        except Exception as e:
            logger.error(f"Failed to initialize YOLOv8 detector: {e}")
            self.yolo_model = None
    
    def _initialize_deepsort_trackers(self):
        """Initialize DeepSORT trackers for each camera."""
        try:
            # Initialize DeepSORT trackers for each camera
            self.trackers = {
                'camera1': DeepSort(
                    max_age=DEEPSORT_MAX_AGE,
                    n_init=DEEPSORT_N_INIT,
                    nms_max_overlap=DEEPSORT_NMS_MAX_OVERLAP,
                    max_cosine_distance=DEEPSORT_MAX_COSINE_DISTANCE,
                    nn_budget=None,
                    override_track_class=None,
                    embedder=DEEPSORT_EMBEDDER,
                    half=DEEPSORT_HALF,
                    bgr=DEEPSORT_BGR,
                    embedder_gpu=DEEPSORT_EMBEDDER_GPU,
                    embedder_model_name=None,
                    embedder_wts=None,
                    polygon=False,
                    today=None
                ),
                'camera2': DeepSort(
                    max_age=DEEPSORT_MAX_AGE,
                    n_init=DEEPSORT_N_INIT,
                    nms_max_overlap=DEEPSORT_NMS_MAX_OVERLAP,
                    max_cosine_distance=DEEPSORT_MAX_COSINE_DISTANCE,
                    nn_budget=None,
                    override_track_class=None,
                    embedder=DEEPSORT_EMBEDDER,
                    half=DEEPSORT_HALF,
                    bgr=DEEPSORT_BGR,
                    embedder_gpu=DEEPSORT_EMBEDDER_GPU,
                    embedder_model_name=None,
                    embedder_wts=None,
                    polygon=False,
                    today=None
                )
            }
            
            logger.info("DeepSORT trackers initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize DeepSORT trackers: {e}")
            self.trackers = {}
    
    def detect_objects(self, frame: np.ndarray, camera_id: str) -> List[DetectedObject]:
        """
        Detect objects in a frame using YOLOv8.
        
        Args:
            frame: Input frame
            camera_id: ID of the camera
            
        Returns:
            List of detected objects
        """
        if self.yolo_model is None:
            logger.warning("YOLO model is None, cannot detect objects")
            return []
        
        try:
            # Run YOLOv8 detection
            logger.debug(f"Running YOLOv8 detection on {camera_id} frame with shape {frame.shape}")
            results = self.yolo_model(frame, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
            
            detected_objects = []
            total_detections = 0
            filtered_by_class = 0
            filtered_by_size = 0
            
            # Process detection results
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    total_detections += len(boxes)
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                        
                        # Get confidence and class
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.yolo_model.names[class_id]
                        
                        logger.debug(f"Raw detection: {class_name} (conf: {confidence:.2f}) at ({x}, {y}, {w}, {h})")
                        
                        # Filter by class
                        if class_name in TRACK_CLASSES:
                            # Filter by size
                            area = w * h
                            if MIN_OBJECT_SIZE <= area <= MAX_OBJECT_SIZE:
                                obj = DetectedObject((x, y, w, h), confidence, class_id, class_name, camera_id)
                                detected_objects.append(obj)
                                logger.debug(f"Accepted detection: {class_name} (conf: {confidence:.2f}) area: {area}")
                            else:
                                filtered_by_size += 1
                                logger.debug(f"Filtered by size: {class_name} area {area} not in range [{MIN_OBJECT_SIZE}, {MAX_OBJECT_SIZE}]")
                        else:
                            filtered_by_class += 1
                            logger.debug(f"Filtered by class: {class_name} not in {TRACK_CLASSES}")
            
            # Log detection summary
            if total_detections > 0:
                logger.info(f"{camera_id}: YOLO detected {total_detections} objects, "
                          f"filtered {filtered_by_class} by class, {filtered_by_size} by size, "
                          f"accepted {len(detected_objects)}")
            else:
                logger.debug(f"{camera_id}: YOLO detected 0 objects")
            
            return detected_objects
            
        except Exception as e:
            logger.error(f"Error in YOLOv8 object detection for {camera_id}: {e}")
            return []
    
    def track_objects(self, frame1: np.ndarray, frame2: np.ndarray) -> Dict[str, List[DetectedObject]]:
        """
        Track objects across both camera frames using DeepSORT.
        
        Args:
            frame1: Frame from camera 1 (can be None)
            frame2: Frame from camera 2 (can be None)
            
        Returns:
            Dictionary with tracked objects for each camera
        """
        tracked_objects1 = []
        tracked_objects2 = []
        
        # Detect objects in frame1 if available
        if frame1 is not None:
            objects1 = self.detect_objects(frame1, "camera1")
            tracked_objects1 = self._update_deepsort_tracking(frame1, objects1, "camera1")
        
        # Detect objects in frame2 if available
        if frame2 is not None:
            objects2 = self.detect_objects(frame2, "camera2")
            tracked_objects2 = self._update_deepsort_tracking(frame2, objects2, "camera2")
        
        # Calculate 3D positions for tracked objects (only if both cameras have objects)
        if tracked_objects1 and tracked_objects2:
            self._calculate_3d_positions(tracked_objects1, tracked_objects2)
        
        return {
            "camera1": tracked_objects1,
            "camera2": tracked_objects2
        }
    
    def _update_deepsort_tracking(self, frame: np.ndarray, detected_objects: List[DetectedObject], camera_id: str) -> List[DetectedObject]:
        """
        Update object tracking using DeepSORT for a specific camera.
        
        Args:
            frame: Input frame
            detected_objects: List of detected objects
            camera_id: ID of the camera
            
        Returns:
            List of tracked objects with track IDs
        """
        if camera_id not in self.trackers:
            return detected_objects
        
        try:
            # Convert detected objects to DeepSORT format
            detections = []
            for obj in detected_objects:
                x, y, w, h = obj.bbox
                detections.append(([x, y, w, h], obj.confidence, obj.class_name))
            
            # Update DeepSORT tracker
            tracks = self.trackers[camera_id].update_tracks(detections, frame=frame)
            
            # Convert tracks back to DetectedObject format
            tracked_objects = []
            for track in tracks:
                if not track.is_confirmed():
                    continue
                
                # Get track information
                track_id = track.track_id
                bbox = track.to_tlbr()  # top left bottom right
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])
                
                # Find corresponding detected object
                best_obj = None
                best_iou = 0
                
                for obj in detected_objects:
                    iou = self._calculate_iou(obj.bbox, (x, y, w, h))
                    if iou > best_iou:
                        best_iou = iou
                        best_obj = obj
                
                if best_obj is not None:
                    # Update the detected object with track ID
                    best_obj.track_id = track_id
                    best_obj.bbox = (x, y, w, h)  # Use refined bbox from tracker
                    tracked_objects.append(best_obj)
                    
                    # Update tracking history
                    if track_id not in self.object_history:
                        self.object_history[track_id] = []
                    self.object_history[track_id].append(best_obj)
                    
                    # Keep only recent history
                    if len(self.object_history[track_id]) > TRACKING_HISTORY_LENGTH:
                        self.object_history[track_id] = self.object_history[track_id][-TRACKING_HISTORY_LENGTH:]
            
            return tracked_objects
            
        except Exception as e:
            logger.error(f"Error in DeepSORT tracking for {camera_id}: {e}")
            return detected_objects
    
    def _calculate_iou(self, bbox1: Tuple[int, int, int, int], bbox2: Tuple[int, int, int, int]) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes.
        
        Args:
            bbox1: First bounding box (x, y, w, h)
            bbox2: Second bounding box (x, y, w, h)
            
        Returns:
            IoU value
        """
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        
        # Calculate intersection
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection = (x_right - x_left) * (y_bottom - y_top)
        
        # Calculate union
        area1 = w1 * h1
        area2 = w2 * h2
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_3d_positions(self, objects1: List[DetectedObject], objects2: List[DetectedObject]):
        """Calculate 3D positions of tracked objects using stereo vision."""
        # Calculate 3D positions for each object from each camera independently
        # Each recognized object is treated as a separate object regardless of similarity
        
        # Calculate 3D positions for objects from camera 1
        for obj1 in objects1:
            # For each object in camera 1, try to find a corresponding object in camera 2
            # If found, use triangulation; if not, estimate position using single camera
            best_match = None
            best_similarity = 0
            
            for obj2 in objects2:
                # Calculate similarity based on class and position
                if obj1.class_name == obj2.class_name:
                    # Simple similarity based on vertical position (assuming cameras are at same height)
                    center1 = obj1.get_center()
                    center2 = obj2.get_center()
                    y_diff = abs(center1[1] - center2[1])
                    similarity = 1.0 / (1.0 + y_diff / FRAME_HEIGHT)  # Normalize by frame height
                    
                    if similarity > best_similarity and similarity > 0.3:  # Threshold for matching
                        best_similarity = similarity
                        best_match = obj2
            
            # Calculate 3D position
            if best_match is not None:
                # Use triangulation with matched object
                pos_3d = self._triangulate_position(obj1, best_match)
            else:
                # Estimate position using single camera (assume object is at typical depth)
                pos_3d = self._estimate_single_camera_position(obj1, "camera1")
            
            if pos_3d is not None:
                obj1.position_3d = pos_3d
        
        # Calculate 3D positions for objects from camera 2
        for obj2 in objects2:
            # Check if this object already has a 3D position from triangulation
            if obj2.position_3d is None:
                # Estimate position using single camera
                pos_3d = self._estimate_single_camera_position(obj2, "camera2")
                if pos_3d is not None:
                    obj2.position_3d = pos_3d
    
    def _triangulate_position(self, obj1: DetectedObject, obj2: DetectedObject) -> Optional[Tuple[float, float, float]]:
        """
        Calculate 3D position using triangulation.
        
        Args:
            obj1: Object from camera 1
            obj2: Object from camera 2
            
        Returns:
            3D position (x, y, z) or None if calculation fails
        """
        try:
            # Get centers of objects
            center1 = obj1.get_center()
            center2 = obj2.get_center()
            
            # Convert pixel coordinates to normalized coordinates
            x1 = (center1[0] - FRAME_WIDTH // 2) / (FRAME_WIDTH // 2)
            y1 = (center1[1] - FRAME_HEIGHT // 2) / (FRAME_HEIGHT // 2)
            x2 = (center2[0] - FRAME_WIDTH // 2) / (FRAME_WIDTH // 2)
            y2 = (center2[1] - FRAME_HEIGHT // 2) / (FRAME_HEIGHT // 2)
            
            # Simple triangulation (assumes cameras are parallel and at same height)
            # This is a simplified calculation - real applications need proper calibration
            
            # Calculate depth using disparity
            disparity = abs(x1 - x2)
            if disparity < 0.01:  # Avoid division by zero
                return None
            
            # Simplified depth calculation
            depth = CAMERA_DISTANCE / disparity
            
            # Calculate 3D position
            x_3d = (x1 + x2) * depth / 2
            y_3d = (y1 + y2) * depth / 2
            z_3d = depth
            
            return (x_3d, y_3d, z_3d)
            
        except Exception as e:
            logger.error(f"Error in triangulation: {e}")
            return None
    
    def _estimate_single_camera_position(self, obj: DetectedObject, camera_id: str) -> Optional[Tuple[float, float, float]]:
        """
        Estimate 3D position for an object detected by only one camera.
        
        Args:
            obj: Detected object
            camera_id: ID of the camera that detected the object
            
        Returns:
            3D position (x, y, z) or None if calculation fails
        """
        try:
            # Get center of object
            center = obj.get_center()
            
            # Convert pixel coordinates to normalized coordinates
            x_norm = (center[0] - FRAME_WIDTH // 2) / (FRAME_WIDTH // 2)
            y_norm = (center[1] - FRAME_HEIGHT // 2) / (FRAME_HEIGHT // 2)
            
            # Estimate depth based on object size (larger objects are closer)
            # This is a simplified estimation - in practice you'd use more sophisticated methods
            area = obj.get_area()
            max_area = FRAME_WIDTH * FRAME_HEIGHT * 0.1  # Assume max 10% of frame area
            depth_factor = max(0.1, min(1.0, area / max_area))  # Normalize between 0.1 and 1.0
            
            # Assume typical depth range (in meters)
            min_depth = 1.0  # 1 meter
            max_depth = 10.0  # 10 meters
            estimated_depth = min_depth + (max_depth - min_depth) * (1.0 - depth_factor)
            
            # Calculate 3D position
            if camera_id == "camera1":
                # Camera 1 is on the left
                x_3d = -CAMERA_DISTANCE / 2 + x_norm * estimated_depth
            else:
                # Camera 2 is on the right
                x_3d = CAMERA_DISTANCE / 2 + x_norm * estimated_depth
            
            y_3d = y_norm * estimated_depth
            z_3d = estimated_depth
            
            return (x_3d, y_3d, z_3d)
            
        except Exception as e:
            logger.error(f"Error in single camera position estimation: {e}")
            return None
    
    def get_tracked_objects(self) -> Dict[str, List[DetectedObject]]:
        """
        Get all currently tracked objects.
        
        Returns:
            Dictionary with tracked objects for each camera
        """
        camera1_objects = []
        camera2_objects = []
        
        for track_info in self.tracked_objects.values():
            if track_info['last_object'] is not None:
                if track_info['camera_id'] == 'camera1':
                    camera1_objects.append(track_info['last_object'])
                else:
                    camera2_objects.append(track_info['last_object'])
        
        return {
            "camera1": camera1_objects,
            "camera2": camera2_objects
        }
    
    def draw_detections(self, frame: np.ndarray, objects: List[DetectedObject]) -> np.ndarray:
        """
        Draw detection boxes and tracking information on frame.
        
        Args:
            frame: Input frame
            objects: List of detected objects
            
        Returns:
            Frame with drawings
        """
        result = frame.copy()
        
        for obj in objects:
            x, y, w, h = obj.bbox
            
            # Draw bounding box
            color = (0, 255, 0) if obj.track_id is not None else (0, 0, 255)
            cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
            
            # Draw track ID, class name, and confidence
            if obj.track_id is not None:
                label = f"ID: {obj.track_id} {obj.class_name} ({obj.confidence:.2f})"
                cv2.putText(result, label, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            else:
                label = f"{obj.class_name} ({obj.confidence:.2f})"
                cv2.putText(result, label, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw 3D position if available
            if obj.position_3d is not None:
                x_3d, y_3d, z_3d = obj.position_3d
                pos_label = f"({x_3d:.2f}, {y_3d:.2f}, {z_3d:.2f})"
                cv2.putText(result, pos_label, (x, y + h + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        return result


if __name__ == "__main__":
    # Test object tracker
    tracker = ObjectTracker()
    print("YOLOv8 + DeepSORT object tracker initialized successfully!") 