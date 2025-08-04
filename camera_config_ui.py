"""
Camera Configuration Interface

Provides a GUI for configuring camera devices and URLs before starting the application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
import json
import os
from typing import Optional, Dict, List
import logging
from config import *

logger = logging.getLogger(__name__)


class CameraConfigUI:
    """Camera configuration interface."""
    
    def __init__(self):
        """Initialize the camera configuration interface."""
        self.root = None
        self.running = False
        
        # Camera configuration
        self.camera_config = {
            'camera1': {
                'type': 'device',  # 'device' or 'url'
                'device_index': 0,
                'url': '',
                'name': 'Camera 1',
                'enabled': True
            },
            'camera2': {
                'type': 'device',
                'device_index': 1,
                'url': '',
                'name': 'Camera 2',
                'enabled': True
            }
        }
        
        # Test camera instances
        self.test_cameras = {}
        self.test_frames = {}
        self.preview_threads = {}  # Track preview threads
        
        # GUI elements
        self.camera_frames = {}
        self.preview_labels = {}
        self.device_vars = {}
        self.url_vars = {}
        self.enable_vars = {}
        self.name_vars = {}
        self.type_vars = {}  # Store type selection variables
        
    def start(self):
        """Start the camera configuration interface."""
        try:
            self.root = tk.Tk()
            self.root.title("Camera Configuration Tool")
            self.root.geometry("800x650")
            self.root.resizable(True, True)
            self.root.protocol("WM_DELETE_WINDOW", self.stop)
            
            # Load existing configuration
            self._load_config()
            
            self._create_widgets()
            self._create_menu()
            
            self.running = True
            self._update_previews()
            
            logger.info("Camera configuration interface started")
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error starting camera configuration: {e}")
            messagebox.showerror("Error", f"Failed to start camera configuration: {e}")
    
    def _create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Camera Configuration Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Help text
        help_label = ttk.Label(main_frame, text="Configure your camera setup. After saving, run 'python main.py' to start the application.", 
                              font=("Arial", 9), foreground="gray")
        help_label.grid(row=1, column=0, pady=(0, 20))
        
        # Camera configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Camera Settings", padding="10")
        config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create camera configuration widgets
        self._create_camera_config_widgets(config_frame)
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Test Cameras", 
                  command=self._test_cameras).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self._save_config).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Load Configuration", 
                  command=self._load_config_dialog).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Done", 
                  command=self.stop).grid(row=0, column=3, padx=5)
    
    def _create_camera_config_widgets(self, parent):
        """Create camera configuration widgets."""
        # Camera 1 configuration
        camera1_frame = ttk.LabelFrame(parent, text="Camera 1", padding="10")
        camera1_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self._create_single_camera_widgets(camera1_frame, 'camera1')
        
        # Camera 2 configuration
        camera2_frame = ttk.LabelFrame(parent, text="Camera 2", padding="10")
        camera2_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._create_single_camera_widgets(camera2_frame, 'camera2')
        
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def _create_single_camera_widgets(self, parent, camera_id):
        """Create widgets for a single camera."""
        # Enable checkbox
        self.enable_vars[camera_id] = tk.BooleanVar(value=self.camera_config[camera_id]['enabled'])
        ttk.Checkbutton(parent, text="Enable Camera", 
                       variable=self.enable_vars[camera_id]).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Camera name
        ttk.Label(parent, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.name_vars[camera_id] = tk.StringVar(value=self.camera_config[camera_id]['name'])
        ttk.Entry(parent, textvariable=self.name_vars[camera_id], width=20).grid(row=1, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        
        # Camera type selection
        ttk.Label(parent, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.type_vars[camera_id] = tk.StringVar(value=self.camera_config[camera_id]['type'])
        type_combo = ttk.Combobox(parent, textvariable=self.type_vars[camera_id], values=['device', 'url'], 
                                 state='readonly', width=15)
        type_combo.grid(row=2, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        type_combo.bind('<<ComboboxSelected>>', lambda e, cid=camera_id: self._on_type_changed(cid, self.type_vars[camera_id].get()))
        
        # Device selection
        device_frame = ttk.Frame(parent)
        device_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(device_frame, text="Device:").grid(row=0, column=0, sticky=tk.W)
        self.device_vars[camera_id] = tk.StringVar(value=str(self.camera_config[camera_id]['device_index']))
        device_combo = ttk.Combobox(device_frame, textvariable=self.device_vars[camera_id], 
                                   values=self._get_available_devices(), width=10)
        device_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # URL input
        url_frame = ttk.Frame(parent)
        url_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_vars[camera_id] = tk.StringVar(value=self.camera_config[camera_id]['url'])
        url_entry = ttk.Entry(url_frame, textvariable=self.url_vars[camera_id], width=30)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # File browser button for URL
        ttk.Button(url_frame, text="Browse", 
                  command=lambda cid=camera_id: self._browse_video_file(cid)).grid(row=0, column=2, padx=(5, 0))
        
        # Help button for URL configuration
        ttk.Button(url_frame, text="?", width=3,
                  command=lambda: self._show_url_help()).grid(row=0, column=3, padx=(5, 0))
        
        # Configure URL frame weights
        url_frame.columnconfigure(1, weight=1)
        
        # Show/hide appropriate widgets based on type
        self._update_camera_widgets_visibility(camera_id, self.camera_config[camera_id]['type'])
        
        # Preview frame
        preview_frame = ttk.LabelFrame(parent, text="Preview", padding="5")
        preview_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.preview_labels[camera_id] = ttk.Label(preview_frame, text="No preview", 
                                                  borderwidth=1, relief="solid", width=40)
        self.preview_labels[camera_id].grid(row=0, column=0)
        
        # Configure parent weights
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(5, weight=1)
    
    def _get_available_devices(self) -> List[str]:
        """Get list of available camera devices."""
        devices = []
        for i in range(10):  # Check first 10 devices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                devices.append(str(i))
                cap.release()
        return devices
    
    def _on_type_changed(self, camera_id: str, camera_type: str):
        """Handle camera type change."""
        self.camera_config[camera_id]['type'] = camera_type
        self._update_camera_widgets_visibility(camera_id, camera_type)
    
    def _update_camera_widgets_visibility(self, camera_id: str, camera_type: str):
        """Update widget visibility based on camera type."""
        try:
            # Get the parent frame (camera1_frame or camera2_frame)
            parent = None
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ttk.LabelFrame) and camera_id.replace('camera', 'Camera ') in grandchild.cget('text'):
                                    parent = grandchild
                                    break
                            if parent:
                                break
                        if parent:
                            break
                if parent:
                    break
            
            if parent:
                # Find device and URL frames
                device_frame = None
                url_frame = None
                
                for child in parent.winfo_children():
                    if isinstance(child, ttk.Frame):
                        # Check if this is the device frame (has "Device:" label)
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Label) and grandchild.cget('text') == 'Device:':
                                device_frame = child
                                break
                        if device_frame:
                            break
                
                # Find URL frame (next frame after device frame)
                if device_frame:
                    for i, child in enumerate(parent.winfo_children()):
                        if child == device_frame and i + 1 < len(parent.winfo_children()):
                            url_frame = parent.winfo_children()[i + 1]
                            break
                
                # Show/hide frames based on camera type
                if device_frame:
                    if camera_type == 'device':
                        device_frame.grid()
                    else:
                        device_frame.grid_remove()
                
                if url_frame:
                    if camera_type == 'url':
                        url_frame.grid()
                    else:
                        url_frame.grid_remove()
                        
        except Exception as e:
            logger.error(f"Error updating camera widgets visibility for {camera_id}: {e}")
    
    def _browse_video_file(self, camera_id: str):
        """Browse for video file."""
        file_path = filedialog.askopenfilename(
            title=f"Select video file for {camera_id}",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            # Convert to file URL format
            file_url = f"file:///{file_path.replace(':', '|')}"
            self.url_vars[camera_id].set(file_url)
    
    def _test_cameras(self):
        """Test camera connections."""
        try:
            # Stop any existing test cameras
            self._stop_test_cameras()
            
            # Test each enabled camera
            for camera_id in ['camera1', 'camera2']:
                if self.enable_vars[camera_id].get():
                    self._test_single_camera(camera_id)
            
            messagebox.showinfo("Success", "Camera testing started. Check previews for live feeds.")
            
        except Exception as e:
            logger.error(f"Error testing cameras: {e}")
            messagebox.showerror("Error", f"Failed to test cameras: {e}")
    
    def _test_single_camera(self, camera_id: str):
        """Test a single camera."""
        try:
            # Get camera configuration
            config = self._get_camera_config(camera_id)
            
            if config['type'] == 'device':
                # Test device camera
                cap = cv2.VideoCapture(int(config['device_index']))
                if not cap.isOpened():
                    raise Exception(f"Could not open device {config['device_index']}")
            else:
                # Test URL camera with proper formatting
                from camera_manager import CameraStream
                temp_camera = CameraStream(config['url'], f"Test_{camera_id}", 'url')
                if not temp_camera.start():
                    raise Exception(f"Could not open URL: {config['url']}")
                cap = temp_camera.cap
                # Don't store temp_camera, just use its cap
            
            # Store camera instance
            self.test_cameras[camera_id] = cap
            
            # Start preview thread
            thread = threading.Thread(target=self._preview_thread, args=(camera_id,), daemon=True)
            thread.start()
            self.preview_threads[camera_id] = thread
            
        except Exception as e:
            logger.error(f"Error testing camera {camera_id}: {e}")
            messagebox.showerror("Error", f"Failed to test {camera_id}: {e}")
    
    def _preview_thread(self, camera_id: str):
        """Thread for camera preview."""
        try:
            cap = self.test_cameras.get(camera_id)
            if cap is None:
                return
                
            while camera_id in self.test_cameras and cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Resize frame for preview
                    preview_frame = cv2.resize(frame, (320, 240))
                    
                    # Convert BGR to RGB
                    rgb_frame = cv2.cvtColor(preview_frame, cv2.COLOR_BGR2RGB)
                    
                    # Convert to PIL Image
                    pil_image = Image.fromarray(rgb_frame)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update preview label (thread-safe)
                    self.root.after(0, lambda: self._update_preview_label(camera_id, photo))
                
                time.sleep(0.033)  # ~30 FPS
                
        except Exception as e:
            logger.error(f"Error in preview thread for {camera_id}: {e}")
        finally:
            # Clean up thread tracking
            if camera_id in self.preview_threads:
                del self.preview_threads[camera_id]
    
    def _update_preview_label(self, camera_id: str, photo):
        """Update preview label (called from main thread)."""
        try:
            if camera_id in self.preview_labels:
                self.preview_labels[camera_id].configure(image=photo)
                self.preview_labels[camera_id].image = photo
        except Exception as e:
            logger.error(f"Error updating preview for {camera_id}: {e}")
    
    def _update_previews(self):
        """Update camera previews."""
        if not self.running:
            return
        
        # Schedule next update
        self.root.after(100, self._update_previews)
    
    def _get_camera_config(self, camera_id: str) -> Dict:
        """Get current camera configuration."""
        camera_type = self.type_vars[camera_id].get()
        
        return {
            'type': camera_type,
            'device_index': int(self.device_vars[camera_id].get()) if camera_type == 'device' else 0,
            'url': self.url_vars[camera_id].get(),
            'name': self.name_vars[camera_id].get(),
            'enabled': self.enable_vars[camera_id].get()
        }
    
    def _save_config(self):
        """Save camera configuration."""
        try:
            # Update configuration from GUI
            for camera_id in ['camera1', 'camera2']:
                self.camera_config[camera_id] = self._get_camera_config(camera_id)
            
            # Save to file
            config_file = 'camera_config.json'
            with open(config_file, 'w') as f:
                json.dump(self.camera_config, f, indent=2)
            
            # Update config.py with camera indices
            self._update_config_py()
            
            messagebox.showinfo("Success", f"Configuration saved to {config_file}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def _update_config_py(self):
        """Update config.py with camera configuration."""
        try:
            # Read current config.py
            with open('config.py', 'r') as f:
                content = f.read()
            
            # Update camera indices
            camera1_index = self.camera_config['camera1']['device_index'] if self.camera_config['camera1']['type'] == 'device' else 0
            camera2_index = self.camera_config['camera2']['device_index'] if self.camera_config['camera2']['type'] == 'device' else 1
            
            # Replace camera indices in config.py
            import re
            content = re.sub(r'CAMERA_1_INDEX = \d+', f'CAMERA_1_INDEX = {camera1_index}', content)
            content = re.sub(r'CAMERA_2_INDEX = \d+', f'CAMERA_2_INDEX = {camera2_index}', content)
            
            # Write updated config.py
            with open('config.py', 'w') as f:
                f.write(content)
            
        except Exception as e:
            logger.error(f"Error updating config.py: {e}")
    
    def _load_config(self):
        """Load camera configuration from file."""
        try:
            config_file = 'camera_config.json'
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.camera_config = json.load(f)
                    
                # Update GUI with loaded configuration
                self._update_gui_from_config()
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def _load_config_dialog(self):
        """Load configuration from file dialog."""
        try:
            config_file = filedialog.askopenfilename(
                title="Load camera configuration",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if config_file:
                with open(config_file, 'r') as f:
                    self.camera_config = json.load(f)
                
                self._update_gui_from_config()
                messagebox.showinfo("Success", f"Configuration loaded from {config_file}")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def _update_gui_from_config(self):
        """Update GUI elements from loaded configuration."""
        try:
            for camera_id in ['camera1', 'camera2']:
                config = self.camera_config[camera_id]
                
                if camera_id in self.name_vars:
                    self.name_vars[camera_id].set(config['name'])
                if camera_id in self.device_vars:
                    self.device_vars[camera_id].set(str(config['device_index']))
                if camera_id in self.url_vars:
                    self.url_vars[camera_id].set(config['url'])
                if camera_id in self.enable_vars:
                    self.enable_vars[camera_id].set(config['enabled'])
                if camera_id in self.type_vars:
                    self.type_vars[camera_id].set(config['type'])
                    
        except Exception as e:
            logger.error(f"Error updating GUI from config: {e}")
    
    def _stop_test_cameras(self):
        """Stop all test cameras."""
        # Create a copy of the keys to avoid "dictionary changed size during iteration" error
        camera_ids = list(self.test_cameras.keys())
        
        for camera_id in camera_ids:
            try:
                cap = self.test_cameras.get(camera_id)
                if cap is not None and cap.isOpened():
                    cap.release()
                # Remove from dictionary safely
                if camera_id in self.test_cameras:
                    del self.test_cameras[camera_id]
            except Exception as e:
                logger.error(f"Error stopping test camera {camera_id}: {e}")
                # Still try to remove from dictionary even if there's an error
                if camera_id in self.test_cameras:
                    del self.test_cameras[camera_id]
        
        # Wait for preview threads to finish
        for camera_id, thread in list(self.preview_threads.items()):
            try:
                if thread.is_alive():
                    thread.join(timeout=1.0)  # Wait up to 1 second
            except Exception as e:
                logger.error(f"Error waiting for preview thread {camera_id}: {e}")
        
        # Clear thread tracking
        self.preview_threads.clear()
    
    def _create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Configuration", command=self._save_config)
        file_menu.add_command(label="Load Configuration", command=self._load_config_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.stop)
        
        # Camera menu
        camera_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Camera", menu=camera_menu)
        camera_menu.add_command(label="Test Cameras", command=self._test_cameras)
        camera_menu.add_command(label="Refresh Device List", command=self._refresh_devices)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="URL Configuration Help", command=self._show_url_help)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _refresh_devices(self):
        """Refresh available device list."""
        try:
            devices = self._get_available_devices()
            for camera_id in ['camera1', 'camera2']:
                if camera_id in self.device_vars:
                    current_value = self.device_vars[camera_id].get()
                    self.device_vars[camera_id].set(current_value)
            
            messagebox.showinfo("Success", f"Found {len(devices)} available devices: {', '.join(devices)}")
            
        except Exception as e:
            logger.error(f"Error refreshing devices: {e}")
            messagebox.showerror("Error", f"Failed to refresh devices: {e}")
    
    def _show_url_help(self):
        """Show URL configuration help."""
        help_text = """
IP Webcam URL Configuration Help
================================

For IP Webcam Android App:
• Basic format: IP_ADDRESS:PORT/video
• Example: 192.168.1.100:8080/video
• Alternative: 192.168.1.100:8080/shot.jpg

For other IP cameras:
• RTSP: rtsp://IP:PORT/stream
• HTTP: http://IP:PORT/videofeed
• MJPEG: http://IP:PORT/mjpeg

Common IP Webcam App URLs:
• Video stream: IP:PORT/video
• Single image: IP:PORT/shot.jpg
• MJPEG stream: IP:PORT/mjpeg

Tips:
• Make sure your phone and computer are on the same network
• Check the IP Webcam app for the correct URL
• Try both /video and /shot.jpg endpoints
• Some apps use different ports (8080, 8081, etc.)
        """
        messagebox.showinfo("URL Configuration Help", help_text)
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """Camera Configuration Tool

A configuration tool for setting up camera devices and URLs
before running the multi-camera object tracking application.

Features:
- Device camera selection
- URL/RTSP stream configuration
- Video file selection
- Camera testing and preview
- Configuration save/load

After configuration, run 'python main.py' to start the application.

Version: 1.0
"""
        messagebox.showinfo("About", about_text)
    
    def stop(self):
        """Stop the configuration interface."""
        self.running = False
        self._stop_test_cameras()
        
        if self.root:
            self.root.quit()
        
        logger.info("Camera configuration interface stopped")


def main():
    """Main entry point for camera configuration."""
    app = CameraConfigUI()
    app.start()


if __name__ == "__main__":
    main() 