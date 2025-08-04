"""
Test Demo Script

Demonstrates the multi-camera object tracking system using simulated camera feeds.
This script can be used to test the system without actual cameras.
"""

import cv2
import numpy as np
import time
import threading
from camera_manager import CameraManager, CameraStream
from object_tracker import ObjectTracker
from visualizer import Visualizer
from config import *

class SimulatedCameraStream(CameraStream):
    """Simulated camera stream for testing purposes."""
    
    def __init__(self, camera_index: int, name: str):
        super().__init__(camera_index, name)
        self.frame_counter = 0
        
    def start(self) -> bool:
        """Start simulated camera stream."""
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        print(f"Simulated camera {self.name} started")
        return True
    
    def _update(self):
        """Generate simulated frames."""
        while not self.stopped:
            try:
                # Create a simulated frame
                frame = self._generate_frame()
                
                with self.lock:
                    self.frame = frame.copy()
                    self.last_frame_time = time.time()
                
                # Calculate FPS
                self.fps_counter += 1
                if self.fps_counter % 30 == 0:
                    self.fps = 30 / (time.time() - self.last_frame_time + 0.001)
                
                time.sleep(1.0 / FPS)  # Simulate frame rate
                
            except Exception as e:
                print(f"Error in simulated camera {self.name}: {e}")
                time.sleep(0.01)
    
    def _generate_frame(self):
        """Generate a simulated frame with moving objects."""
        # Create a black frame
        frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        
        # Add some background noise
        frame += np.random.randint(0, 30, frame.shape, dtype=np.uint8)
        
        # Add moving objects
        time_val = time.time()
        
        # Object 1 - moving in a circle
        center_x = FRAME_WIDTH // 2 + int(100 * np.cos(time_val))
        center_y = FRAME_HEIGHT // 2 + int(50 * np.sin(time_val))
        cv2.circle(frame, (center_x, center_y), 30, (0, 255, 0), -1)
        
        # Object 2 - moving horizontally
        x2 = int((time_val * 50) % FRAME_WIDTH)
        y2 = FRAME_HEIGHT // 3
        cv2.rectangle(frame, (x2, y2), (x2 + 40, y2 + 40), (255, 0, 0), -1)
        
        # Object 3 - moving vertically
        x3 = FRAME_WIDTH // 4
        y3 = int((time_val * 30) % FRAME_HEIGHT)
        cv2.ellipse(frame, (x3, y3), (25, 15), 0, 0, 360, (0, 0, 255), -1)
        
        # Add some text
        cv2.putText(frame, f"Simulated {self.name}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Frame: {self.frame_counter}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        self.frame_counter += 1
        return frame


class SimulatedCameraManager(CameraManager):
    """Camera manager that uses simulated cameras."""
    
    def initialize_cameras(self) -> bool:
        """Initialize simulated cameras."""
        print("Initializing simulated cameras...")
        
        # Initialize simulated camera 1
        camera1 = SimulatedCameraStream(CAMERA_1_INDEX, "Camera 1")
        if not camera1.start():
            print("Failed to start simulated Camera 1")
            return False
        
        # Initialize simulated camera 2
        camera2 = SimulatedCameraStream(CAMERA_2_INDEX, "Camera 2")
        if not camera2.start():
            print("Failed to start simulated Camera 2")
            camera1.stop()
            return False
        
        self.cameras = {
            "camera1": camera1,
            "camera2": camera2
        }
        
        self.running = True
        print("All simulated cameras initialized successfully")
        return True


def run_demo():
    """Run the demo with simulated cameras."""
    print("=" * 60)
    print("Multi-Camera Object Tracking - Demo Mode")
    print("=" * 60)
    print("This demo uses simulated camera feeds to test the system.")
    print("Press 'q' to quit the application.")
    print("=" * 60)
    
    try:
        # Initialize components with simulated cameras
        camera_manager = SimulatedCameraManager()
        if not camera_manager.initialize_cameras():
            print("Failed to initialize simulated cameras")
            return
        
        object_tracker = ObjectTracker()
        visualizer = Visualizer(camera_manager, object_tracker)
        
        # Start the application
        print("Starting demo application...")
        visualizer.start()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error in demo: {e}")
    finally:
        if 'camera_manager' in locals():
            camera_manager.stop_all()
        print("Demo finished")


if __name__ == "__main__":
    run_demo() 