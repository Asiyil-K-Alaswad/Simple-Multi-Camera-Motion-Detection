#!/usr/bin/env python3
"""
Basic IP webcam test script.
Displays the IP webcam feed without object tracking.
"""

import cv2
import numpy as np
import time
import logging
import urllib.request
import urllib.error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasicIPWebcam:
    """Basic IP webcam display class."""
    
    def __init__(self, webcam_url):
        """
        Initialize basic IP webcam.
        
        Args:
            webcam_url: URL of the IP webcam (e.g., "http://192.168.238.47:8080/shot.jpg")
        """
        self.webcam_url = webcam_url
        self.running = False
        self.frame_count = 0
        self.fps_counter = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test IP webcam connection."""
        print(f"Testing connection to: {self.webcam_url}")
        try:
            req = urllib.request.Request(self.webcam_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() == 200:
                    print("✅ IP webcam connection successful")
                    content_type = response.headers.get('Content-Type', '')
                    print(f"   Content-Type: {content_type}")
                else:
                    print(f"❌ HTTP error: {response.getcode()}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise
    
    def get_frame(self):
        """Get a single frame from IP webcam."""
        try:
            req = urllib.request.Request(self.webcam_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() == 200:
                    # Read image data
                    image_data = response.read()
                    
                    # Convert to numpy array
                    nparr = np.frombuffer(image_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        return frame
                    else:
                        logger.warning("Failed to decode image from IP webcam")
                        return None
                else:
                    logger.error(f"HTTP error: {response.getcode()}")
                    return None
                    
        except urllib.error.URLError as e:
            logger.error(f"URL error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting frame: {e}")
            return None
    
    def _calculate_fps(self):
        """Calculate and update FPS."""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.fps_counter / (current_time - self.last_fps_time)
            self.fps_counter = 0
            self.last_fps_time = current_time
    
    def run(self):
        """Main display loop."""
        print("Starting basic IP webcam display...")
        print("Press 'q' to quit, 's' to save frame")
        
        self.running = True
        
        while self.running:
            try:
                # Get frame from IP webcam
                frame = self.get_frame()
                
                if frame is not None:
                    # Calculate FPS
                    self._calculate_fps()
                    
                    # Add info text to frame
                    cv2.putText(frame, f"FPS: {self.fps:.1f}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Frame: {self.frame_count}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Size: {frame.shape[1]}x{frame.shape[0]}", (10, 110), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Display frame
                    cv2.imshow('IP Webcam Feed', frame)
                    
                    self.frame_count += 1
                else:
                    logger.warning("Failed to get frame from IP webcam")
                    # Show error frame
                    error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(error_frame, "No signal from IP webcam", (50, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('IP Webcam Feed', error_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"ipwebcam_basic_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Saved frame as: {filename}")
                
                # Minimal delay for higher framerate
                time.sleep(0.01)  # 10ms delay instead of 100ms
                
            except KeyboardInterrupt:
                print("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)  # Wait before retrying
        
        self.stop()
    
    def stop(self):
        """Stop display and cleanup."""
        self.running = False
        cv2.destroyAllWindows()
        print("IP webcam display stopped")

def main():
    """Main function."""
    # IP webcam URL
    webcam_url = "http://192.168.238.47:8080/shot.jpg"
    
    try:
        # Create and run basic display
        webcam = BasicIPWebcam(webcam_url)
        webcam.run()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Failed to start display: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure the IP webcam app is running")
        print("2. Check the IP address is correct")
        print("3. Ensure both devices are on the same network")
        print("4. Try accessing the URL in a web browser first")

if __name__ == "__main__":
    main() 