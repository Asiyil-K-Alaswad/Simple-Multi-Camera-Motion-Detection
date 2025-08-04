#!/usr/bin/env python3
"""
High-framerate local camera object tracking script.
Uses threading to get frames asynchronously for maximum performance.
"""

import cv2
import numpy as np
import time
import logging
import threading
import queue
from object_tracker import ObjectTracker
from config import *
from deep_sort_realtime.deepsort_tracker import DeepSort

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HighFPSLocalCameraTracker:
    """High-framerate local camera object tracking class."""
    
    def __init__(self, camera_index=0, max_queue_size=10):
        """
        Initialize high-framerate local camera tracker.
        
        Args:
            camera_index: Camera device index (default: 0)
            max_queue_size: Maximum number of frames to buffer
        """
        self.camera_index = camera_index
        self.max_queue_size = max_queue_size
        self.tracker = ObjectTracker()
        
        # Add DeepSORT tracker for local camera
        self.tracker.trackers['local_camera'] = DeepSort(
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
        
        # Threading variables
        self.running = False
        self.frame_queue = queue.Queue(maxsize=max_queue_size)
        self.frame_thread = None
        self.cap = None
        
        # Performance tracking
        self.frame_count = 0
        self.fps_counter = 0
        self.fps = 0
        self.last_fps_time = time.time()
        self.last_frame_time = 0
        self.frame_times = []
        
        # Test camera connection
        self._test_camera()
    
    def _test_camera(self):
        """Test local camera connection."""
        print(f"Testing local camera (index: {self.camera_index})...")
        try:
            cap = cv2.VideoCapture(self.camera_index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print("✅ Local camera connection successful")
                    print(f"   Frame size: {frame.shape[1]}x{frame.shape[0]}")
                    cap.release()
                else:
                    print("❌ Failed to read frame from camera")
                    cap.release()
                    raise Exception("Cannot read from camera")
            else:
                print("❌ Failed to open camera")
                raise Exception("Cannot open camera")
        except Exception as e:
            print(f"❌ Camera test failed: {e}")
            raise
    
    def _frame_fetcher_thread(self):
        """Thread function to continuously fetch frames from camera."""
        print("Starting frame fetcher thread...")
        
        # Open camera in thread
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            logger.error("Failed to open camera in frame fetcher thread")
            return
        
        # Set camera properties for high framerate
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, 30)  # Try to set 30 FPS
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size
        
        while self.running:
            try:
                # Get frame from camera
                ret, frame = self.cap.read()
                
                if ret and frame is not None:
                    # Resize frame to configured size
                    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
                    
                    # Add frame to queue, remove oldest if full
                    if self.frame_queue.full():
                        try:
                            self.frame_queue.get_nowait()  # Remove oldest frame
                        except queue.Empty:
                            pass
                    
                    self.frame_queue.put(frame, timeout=0.1)
                else:
                    # Brief pause if no frame available
                    time.sleep(0.01)
                    
            except Exception as e:
                logger.error(f"Error in frame fetcher thread: {e}")
                time.sleep(0.1)  # Brief pause on error
        
        # Cleanup camera
        if self.cap:
            self.cap.release()
        print("Frame fetcher thread stopped")
    
    def get_frame(self):
        """Get frame from the queue (non-blocking)."""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def process_frame(self, frame):
        """Process frame with object tracking."""
        if frame is None:
            return None
        
        try:
            # Detect objects in the frame
            detected_objects = self.tracker.detect_objects(frame, "local_camera")
            
            # Update tracking with DeepSORT
            tracked_objects = self.tracker._update_deepsort_tracking(frame, detected_objects, "local_camera")
            
            # Draw tracking results
            result_frame = self._draw_tracking_results(frame, tracked_objects)
            
            return result_frame
            
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return frame
    
    def _draw_tracking_results(self, frame, tracked_objects):
        """Draw tracking results on frame."""
        if tracked_objects is None or len(tracked_objects) == 0:
            return frame
        
        # Draw bounding boxes and labels
        for obj in tracked_objects:
            bbox = obj.bbox  # This is a tuple (x, y, w, h)
            track_id = obj.track_id
            class_id = obj.class_id
            confidence = obj.confidence
            class_name = obj.class_name
            
            # Convert bbox to x1, y1, x2, y2 format for drawing
            x, y, w, h = bbox
            x1, y1, x2, y2 = x, y, x + w, y + h
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name} ID:{track_id} {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), (0, 255, 0), -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame
    
    def _calculate_fps(self):
        """Calculate and update FPS."""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.fps_counter / (current_time - self.last_fps_time)
            self.fps_counter = 0
            self.last_fps_time = current_time
            
            # Calculate average frame time
            if len(self.frame_times) > 0:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                logger.info(f"FPS: {self.fps:.1f}, Avg Frame Time: {avg_frame_time*1000:.1f}ms")
                self.frame_times = []  # Reset for next second
    
    def run(self):
        """Main tracking loop with high framerate."""
        print("Starting high-framerate local camera object tracking...")
        print("Press 'q' to quit, 's' to save frame")
        print(f"Frame buffer size: {self.max_queue_size}")
        
        self.running = True
        
        # Start frame fetcher thread
        self.frame_thread = threading.Thread(target=self._frame_fetcher_thread, daemon=True)
        self.frame_thread.start()
        
        while self.running:
            try:
                # Get frame from queue
                frame = self.get_frame()
                
                if frame is not None:
                    # Record frame time
                    current_time = time.time()
                    if self.last_frame_time > 0:
                        frame_time = current_time - self.last_frame_time
                        self.frame_times.append(frame_time)
                    self.last_frame_time = current_time
                    
                    # Process frame with tracking
                    result_frame = self.process_frame(frame)
                    
                    if result_frame is not None:
                        # Calculate FPS
                        self._calculate_fps()
                        
                        # Add performance info to frame
                        cv2.putText(result_frame, f"FPS: {self.fps:.1f}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(result_frame, f"Frame: {self.frame_count}", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(result_frame, f"Queue: {self.frame_queue.qsize()}/{self.max_queue_size}", (10, 110), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Display frame
                        cv2.imshow('High-FPS Local Camera Tracking', result_frame)
                        
                        self.frame_count += 1
                    else:
                        logger.warning("Failed to process frame")
                else:
                    # No frame available, show status
                    status_frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
                    cv2.putText(status_frame, "Waiting for frames...", (50, FRAME_HEIGHT//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.imshow('High-FPS Local Camera Tracking', status_frame)
                
                # Handle key presses (non-blocking)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"highfps_local_{timestamp}.jpg"
                    cv2.imwrite(filename, result_frame if result_frame is not None else frame)
                    print(f"Saved frame as: {filename}")
                
                # No artificial delay - let it run as fast as possible
                
            except KeyboardInterrupt:
                print("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(0.1)  # Brief pause on error
        
        self.stop()
    
    def stop(self):
        """Stop tracking and cleanup."""
        self.running = False
        
        # Wait for frame thread to finish
        if self.frame_thread and self.frame_thread.is_alive():
            self.frame_thread.join(timeout=2)
        
        cv2.destroyAllWindows()
        if hasattr(self.tracker, 'cleanup'):
            self.tracker.cleanup()
        print("High-framerate local camera tracking stopped")

def main():
    """Main function."""
    try:
        # Create and run high-framerate tracker with local camera
        tracker = HighFPSLocalCameraTracker(camera_index=0, max_queue_size=10)
        tracker.run()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Failed to start tracking: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have a camera connected")
        print("2. Try a different camera index (1, 2, etc.)")
        print("3. Check if the camera is being used by another application")

if __name__ == "__main__":
    main() 