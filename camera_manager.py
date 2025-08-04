"""
Camera Manager Module

Handles camera initialization, threading, and frame retrieval for dual camera setup.
"""

import cv2
import threading
import time
import numpy as np
import json
import os
from typing import Optional, Tuple, Dict
import logging
from config import *

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)


class CameraStream:
    """Individual camera stream with threading support."""
    
    def __init__(self, camera_source: str, name: str, camera_type: str = 'device'):
        """
        Initialize camera stream.
        
        Args:
            camera_source: Camera device index (int) or URL (str)
            name: Camera name for logging
            camera_type: 'device' for device index, 'url' for URL/RTSP stream
        """
        self.camera_source = camera_source
        self.camera_type = camera_type
        self.name = name
        self.cap = None
        self.frame = None
        self.stopped = False
        self.thread = None
        self.lock = threading.Lock()
        self.last_frame_time = 0
        self.fps_counter = 0
        self.fps = 0
        self._shot_jpg_url = None  # Store shot.jpg URL for fallback
        self._mjpeg_error_count = 0  # Count MJPEG boundary errors
        self._max_mjpeg_errors = 5  # Max errors before switching to shot.jpg
        
    def start(self) -> bool:
        """
        Start camera stream in a separate thread.
        
        Returns:
            bool: True if camera started successfully
        """
        try:
            # Open camera based on type
            if self.camera_type == 'device':
                self.cap = cv2.VideoCapture(int(self.camera_source))
            else:  # URL type
                # Format URL for IP webcam compatibility
                formatted_url = self._format_ip_webcam_url(self.camera_source)
                logger.info(f"Opening URL camera {self.name} with formatted URL: {formatted_url}")
                
                # Test URL connectivity first
                if not self._test_url_connectivity(formatted_url):
                    logger.warning(f"URL connectivity test failed for {self.name}, but will try to open anyway")
                
                # Try different approaches for URL cameras
                self.cap = self._open_url_camera(formatted_url)
                
                # Ensure shot.jpg URL is stored for fallback
                if self.camera_type == 'url' and not self._shot_jpg_url:
                    self._shot_jpg_url = formatted_url
                    logger.info(f"Stored shot.jpg URL for {self.name}: {self._shot_jpg_url}")
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera {self.name} at source {self.camera_source}")
                return False
            
            # Set camera properties (only for device cameras)
            if self.camera_type == 'device':
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                self.cap.set(cv2.CAP_PROP_FPS, FPS)
            
            # Start thread
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            
            logger.info(f"Camera {self.name} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting camera {self.name}: {e}")
            return False
    
    def _open_url_camera(self, url: str) -> cv2.VideoCapture:
        """
        Open URL camera with multiple fallback strategies.
        Prioritizes shot.jpg for better reliability with IP webcams.
        
        Args:
            url: Formatted URL
            
        Returns:
            cv2.VideoCapture: OpenCV capture object
        """
        # Ensure URL has proper HTTP protocol
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            logger.info(f"Added HTTP protocol to URL: {url}")
        
        # Strategy 1: Try with shot.jpg endpoint first (most reliable for IP webcams)
        if '/shot.jpg' in url:
            try:
                logger.info(f"Attempting to open shot.jpg URL: {url}")
                cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)  # Explicitly use FFMPEG backend for HTTP
                if cap.isOpened():
                    # Test if we can read a frame
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        logger.info(f"URL camera {self.name} opened successfully with shot.jpg endpoint")
                        # Store the shot.jpg URL for later use
                        self._shot_jpg_url = url
                        return cap
                    else:
                        logger.warning(f"shot.jpg URL opened but failed to read frame")
                        cap.release()
                else:
                    logger.warning(f"Failed to open shot.jpg URL: {url}")
            except Exception as e:
                logger.debug(f"shot.jpg URL opening failed: {e}")
        
        # Strategy 2: Try with FFMPEG backend (preferred for HTTP URLs)
        try:
            logger.info(f"Attempting to open URL with FFMPEG backend: {url}")
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                # Test if we can read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    logger.info(f"URL camera {self.name} opened successfully with FFMPEG backend")
                    return cap
                else:
                    logger.warning(f"FFMPEG URL opened but failed to read frame")
                    cap.release()
            else:
                logger.warning(f"Failed to open URL with FFMPEG backend: {url}")
        except Exception as e:
            logger.debug(f"FFMPEG backend URL opening failed: {e}")
        
        # Strategy 3: Try with default settings (fallback)
        try:
            logger.info(f"Attempting to open URL with default backend: {url}")
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                # Test if we can read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    logger.info(f"URL camera {self.name} opened successfully with default settings")
                    return cap
                else:
                    logger.warning(f"Default URL opened but failed to read frame")
                    cap.release()
            else:
                logger.warning(f"Failed to open URL with default backend: {url}")
        except Exception as e:
            logger.debug(f"Default URL opening failed: {e}")
        
        # Strategy 4: Try with MJPEG-specific settings (least preferred due to boundary issues)
        try:
            logger.info(f"Attempting to open URL with MJPEG settings: {url}")
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                # Set MJPEG-specific properties
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                
                # Test if we can read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    logger.info(f"URL camera {self.name} opened successfully with MJPEG settings")
                    return cap
                else:
                    logger.warning(f"MJPEG URL opened but failed to read frame")
                    cap.release()
            else:
                logger.warning(f"Failed to open URL with MJPEG settings: {url}")
        except Exception as e:
            logger.debug(f"MJPEG URL opening failed: {e}")
        
        # Always store shot.jpg URL for fallback, even if we use video stream
        if '/video' in url:
            self._shot_jpg_url = url.replace('/video', '/shot.jpg')
            logger.info(f"Stored shot.jpg URL for {self.name}: {self._shot_jpg_url}")
        
        # If all strategies fail, return a failed capture
        logger.error(f"All URL opening strategies failed for {self.name} with URL: {url}")
        return cv2.VideoCapture()
    
    def _format_ip_webcam_url(self, url: str) -> str:
        """
        Format URL for IP webcam compatibility.
        
        Args:
            url: Raw URL from configuration
            
        Returns:
            str: Formatted URL for OpenCV
        """
        # Remove any whitespace
        url = url.strip()
        
        # If URL doesn't start with http:// or https://, add http://
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # For IP Webcam Android app, prefer shot.jpg over video for reliability
        # shot.jpg gives single JPEG images, which OpenCV handles much better
        if '/video' in url:
            # Convert video to shot.jpg for better reliability
            url = url.replace('/video', '/shot.jpg')
            logger.info(f"Converting video endpoint to shot.jpg for better reliability: {url}")
        elif '/shot.jpg' in url:
            # Already using shot.jpg - perfect!
            pass
        elif '/videofeed' in url:
            # Convert videofeed to shot.jpg
            url = url.replace('/videofeed', '/shot.jpg')
            logger.info(f"Converting videofeed to shot.jpg for better reliability: {url}")
        elif '/stream' in url:
            # Convert stream to shot.jpg
            url = url.replace('/stream', '/shot.jpg')
            logger.info(f"Converting stream to shot.jpg for better reliability: {url}")
        elif ':' in url and not url.endswith('/'):
            # Add /shot.jpg endpoint if not present
            url = url + '/shot.jpg'
            logger.info(f"Adding shot.jpg endpoint for better reliability: {url}")
        
        logger.debug(f"Formatted URL: {url}")
        return url
    
    def _test_url_connectivity(self, url: str) -> bool:
        """
        Test if URL is accessible.
        
        Args:
            url: URL to test
            
        Returns:
            bool: True if URL is accessible
        """
        try:
            import urllib.request
            import urllib.error
            
            # Try to open the URL
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.getcode() == 200
        except Exception as e:
            logger.debug(f"URL connectivity test failed for {url}: {e}")
            return False
    
    def _get_url_frame(self) -> Optional[np.ndarray]:
        """
        Get frame from URL camera using urllib (fallback method).
        
        Returns:
            np.ndarray: Frame as numpy array, or None if failed
        """
        try:
            import urllib.request
            import urllib.error
            
            if not self._shot_jpg_url:
                return None
            
            # Make HTTP request to get image
            req = urllib.request.Request(self._shot_jpg_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.getcode() == 200:
                    # Read image data
                    image_data = response.read()
                    
                    # Convert to numpy array
                    nparr = np.frombuffer(image_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        return frame
                    else:
                        logger.warning(f"Failed to decode image from {self.name}")
                        return None
                else:
                    logger.error(f"HTTP error {response.getcode()} from {self.name}")
                    return None
                    
        except urllib.error.URLError as e:
            logger.debug(f"URL error for {self.name}: {e}")
            return None
        except Exception as e:
            logger.debug(f"Error getting frame from {self.name}: {e}")
            return None
    
    def _update(self):
        """Update loop for camera frame capture."""
        consecutive_errors = 0
        max_consecutive_errors = 10
        
        while not self.stopped:
            try:
                if self.cap is None or not self.cap.isOpened():
                    logger.error(f"Camera {self.name} is not available")
                    break
                
                # For URL cameras, try to get frame using urllib if OpenCV fails
                if self.camera_type == 'url' and self._shot_jpg_url:
                    frame = self._get_url_frame()
                else:
                    ret, frame = self.cap.read()
                    if not ret or frame is None:
                        frame = None
                
                if frame is not None:
                    # Reset error counter on successful frame
                    consecutive_errors = 0
                    
                    # Resize frame to configured size
                    try:
                        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
                    except Exception as resize_error:
                        logger.warning(f"Frame resize error for {self.name}: {resize_error}")
                        continue
                    
                    with self.lock:
                        self.frame = frame.copy()
                        self.last_frame_time = time.time()
                    
                    # Calculate FPS
                    self.fps_counter += 1
                    if self.fps_counter % 30 == 0:
                        self.fps = 30 / (time.time() - self.last_frame_time + 0.001)
                    
                    # For URL cameras, add minimal delay for better performance
                    if self.camera_type == 'url':
                        time.sleep(0.01)  # 10ms delay for URL cameras
                        
                else:
                    consecutive_errors += 1
                    if consecutive_errors <= 3:
                        logger.warning(f"Failed to read frame from camera {self.name} (attempt {consecutive_errors})")
                    elif consecutive_errors == max_consecutive_errors:
                        logger.error(f"Too many consecutive errors for camera {self.name}, stopping")
                        break
                    
                    time.sleep(0.1)  # Longer sleep for URL cameras
                    
            except cv2.error as cv_error:
                consecutive_errors += 1
                error_msg = str(cv_error)
                
                if ("get_buffer() failed" in error_msg or "pic->data" in error_msg or 
                    "boundary" in error_msg.lower() or "mpjpeg" in error_msg.lower()):
                    # MJPEG-related error - try to recover
                    self._mjpeg_error_count += 1
                    logger.warning(f"MJPEG error for {self.name}: {error_msg} (count: {self._mjpeg_error_count})")
                    
                    if self._mjpeg_error_count >= self._max_mjpeg_errors and self._shot_jpg_url:
                        # Switch to shot.jpg mode
                        logger.info(f"Switching {self.name} to shot.jpg mode due to persistent MJPEG errors")
                        if self._switch_to_shot_jpg_mode():
                            self._mjpeg_error_count = 0  # Reset error count
                            consecutive_errors = 0  # Reset consecutive errors
                        else:
                            logger.error(f"Failed to switch {self.name} to shot.jpg mode")
                    else:
                        logger.info(f"Attempting recovery for {self.name}...")
                        time.sleep(0.5)  # Give more time for buffer recovery
                else:
                    logger.error(f"OpenCV error in camera {self.name} update loop: {cv_error}")
                    time.sleep(0.1)
                    
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Too many consecutive errors for camera {self.name}, stopping")
                    break
                    
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"Error in camera {self.name} update loop: {e}")
                time.sleep(0.1)
                
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Too many consecutive errors for camera {self.name}, stopping")
                    break
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Get the latest frame from camera.
        
        Returns:
            np.ndarray: Latest frame or None if not available
        """
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
        return None
    
    def get_fps(self) -> float:
        """Get current FPS of the camera."""
        return self.fps
    
    def stop(self):
        """Stop camera stream."""
        self.stopped = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=CAMERA_THREAD_TIMEOUT)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        logger.info(f"Camera {self.name} stopped")
    
    def restart(self) -> bool:
        """Restart camera stream (useful for URL cameras)."""
        logger.info(f"Restarting camera {self.name}")
        self.stop()
        time.sleep(1.0)  # Give time for cleanup
        return self.start()
    
    def reconnect(self) -> bool:
        """Reconnect camera with different strategies (for URL cameras)."""
        logger.info(f"Attempting to reconnect camera {self.name}")
        
        if self.camera_type != 'url':
            logger.info(f"Camera {self.name} is not URL type, using normal restart")
            return self.restart()
        
        # Try different URL formats for reconnection
        original_url = self.camera_source
        reconnect_urls = [
            original_url,
            original_url.replace('/video', '/shot.jpg'),
            original_url.replace('/shot.jpg', '/video')
        ]
        
        for url in reconnect_urls:
            logger.info(f"Trying reconnection with URL: {url}")
            
            # Stop current connection
            self.stop()
            time.sleep(1.0)
            
            # Try to reconnect with this URL
            self.camera_source = url
            if self.start():
                logger.info(f"Successfully reconnected {self.name} with URL: {url}")
                return True
            else:
                logger.warning(f"Failed to reconnect {self.name} with URL: {url}")
        
        # If all URLs fail, restore original and try normal restart
        self.camera_source = original_url
        logger.warning(f"All reconnection attempts failed for {self.name}, trying normal restart")
        return self.restart()
    
    def _switch_to_shot_jpg_mode(self) -> bool:
        """Switch to shot.jpg mode for URL cameras."""
        if not self._shot_jpg_url:
            logger.warning(f"No shot.jpg URL available for {self.name}")
            return False
        
        try:
            logger.info(f"Switching {self.name} to shot.jpg mode: {self._shot_jpg_url}")
            
            # Close current capture
            if self.cap:
                self.cap.release()
            
            # Open shot.jpg capture
            self.cap = cv2.VideoCapture(self._shot_jpg_url)
            if not self.cap.isOpened():
                logger.error(f"Failed to open shot.jpg for {self.name}")
                return False
            
            logger.info(f"Successfully switched {self.name} to shot.jpg mode")
            return True
            
        except Exception as e:
            logger.error(f"Error switching {self.name} to shot.jpg mode: {e}")
            return False


class CameraManager:
    """Manages multiple camera streams."""
    
    def __init__(self):
        """Initialize camera manager."""
        self.cameras = {}
        self.running = False
        
    def initialize_cameras(self) -> bool:
        """
        Initialize all cameras.
        
        Returns:
            bool: True if all cameras initialized successfully
        """
        logger.info("Initializing cameras...")
        
        # Load camera configuration
        camera_config = self._load_camera_config()
        
        # Initialize camera 1
        if camera_config['camera1']['enabled']:
            camera1 = CameraStream(
                str(camera_config['camera1']['device_index']) if camera_config['camera1']['type'] == 'device' else camera_config['camera1']['url'],
                camera_config['camera1']['name'],
                camera_config['camera1']['type']
            )
            if not camera1.start():
                logger.error("Failed to start Camera 1")
                return False
        else:
            camera1 = None
            logger.info("Camera 1 is disabled")
        
        # Initialize camera 2
        if camera_config['camera2']['enabled']:
            camera2 = CameraStream(
                str(camera_config['camera2']['device_index']) if camera_config['camera2']['type'] == 'device' else camera_config['camera2']['url'],
                camera_config['camera2']['name'],
                camera_config['camera2']['type']
            )
            if not camera2.start():
                logger.error("Failed to start Camera 2")
                if camera1:
                    camera1.stop()
                return False
        else:
            camera2 = None
            logger.info("Camera 2 is disabled")
        
        self.cameras = {
            "camera1": camera1,
            "camera2": camera2
        }
        
        self.running = True
        logger.info("All cameras initialized successfully")
        return True
    
    def _load_camera_config(self) -> Dict:
        """Load camera configuration from file or use defaults."""
        try:
            config_file = 'camera_config.json'
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                # Return default configuration
                return {
                    'camera1': {
                        'type': 'device',
                        'device_index': CAMERA_1_INDEX,
                        'url': '',
                        'name': 'Camera 1',
                        'enabled': True
                    },
                    'camera2': {
                        'type': 'device',
                        'device_index': CAMERA_2_INDEX,
                        'url': '',
                        'name': 'Camera 2',
                        'enabled': True
                    }
                }
        except Exception as e:
            logger.error(f"Error loading camera configuration: {e}")
            # Return default configuration on error
            return {
                'camera1': {
                    'type': 'device',
                    'device_index': CAMERA_1_INDEX,
                    'url': '',
                    'name': 'Camera 1',
                    'enabled': True
                },
                'camera2': {
                    'type': 'device',
                    'device_index': CAMERA_2_INDEX,
                    'url': '',
                    'name': 'Camera 2',
                    'enabled': True
                }
            }
    
    def get_frames(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Get frames from both cameras.
        
        Returns:
            Tuple: (frame1, frame2) or (None, None) if not available
        """
        if not self.running:
            return None, None
        
        frame1 = self.cameras["camera1"].get_frame() if self.cameras["camera1"] else None
        frame2 = self.cameras["camera2"].get_frame() if self.cameras["camera2"] else None
        
        return frame1, frame2
    
    def get_camera_info(self) -> dict:
        """
        Get information about all cameras.
        
        Returns:
            dict: Camera information including FPS and status
        """
        info = {}
        for name, camera in self.cameras.items():
            if camera is not None:
                info[name] = {
                    "fps": camera.get_fps(),
                    "running": not camera.stopped,
                    "source": camera.camera_source,
                    "type": camera.camera_type,
                    "name": camera.name
                }
            else:
                info[name] = {
                    "fps": 0,
                    "running": False,
                    "source": "disabled",
                    "type": "disabled",
                    "name": "Disabled"
                }
        return info
    
    def stop_all(self):
        """Stop all camera streams."""
        logger.info("Stopping all cameras...")
        self.running = False
        
        for camera in self.cameras.values():
            if camera is not None:
                camera.stop()
        
        self.cameras.clear()
        logger.info("All cameras stopped")


def test_cameras():
    """Test function to check camera availability."""
    logger.info("Testing camera availability...")
    
    # Test camera 1
    cap1 = cv2.VideoCapture(CAMERA_1_INDEX)
    if cap1.isOpened():
        logger.info(f"Camera 1 (index {CAMERA_1_INDEX}) is available")
        cap1.release()
    else:
        logger.warning(f"Camera 1 (index {CAMERA_1_INDEX}) is not available")
    
    # Test camera 2
    cap2 = cv2.VideoCapture(CAMERA_2_INDEX)
    if cap2.isOpened():
        logger.info(f"Camera 2 (index {CAMERA_2_INDEX}) is available")
        cap2.release()
    else:
        logger.warning(f"Camera 2 (index {CAMERA_2_INDEX}) is not available")


if __name__ == "__main__":
    # Test camera functionality
    test_cameras()
    
    # Test camera manager
    manager = CameraManager()
    if manager.initialize_cameras():
        print("Cameras initialized successfully!")
        
        # Run for a few seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            frame1, frame2 = manager.get_frames()
            if frame1 is not None and frame2 is not None:
                print("Frames received successfully")
                break
            time.sleep(0.1)
        
        manager.stop_all()
    else:
        print("Failed to initialize cameras") 