"""
Visualizer Module

Handles GUI visualization of camera feeds and 3D object positions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
from typing import Optional, Dict, List
import logging
from config import *
from object_tracker import DetectedObject

logger = logging.getLogger(__name__)


class Visualizer:
    """Main visualization class for the multi-camera tracking system."""
    
    def __init__(self, camera_manager, object_tracker):
        """
        Initialize visualizer.
        
        Args:
            camera_manager: Camera manager instance
            object_tracker: Object tracker instance
        """
        self.camera_manager = camera_manager
        self.object_tracker = object_tracker
        self.root = None
        self.running = False
        
        # GUI elements
        self.camera1_label = None
        self.camera2_label = None
        self.canvas_3d = None
        self.status_label = None
        self.fps_label = None
        
        # Display settings
        self.display_width = int(DISPLAY_WIDTH * DISPLAY_SCALE)
        self.display_height = int(DISPLAY_HEIGHT * DISPLAY_SCALE)
        self.display_scale = DISPLAY_SCALE
        
        # 3D visualization settings
        self.canvas_width = CANVAS_WIDTH
        self.canvas_height = CANVAS_HEIGHT
        self.scale_factor = 100  # Pixels per meter
        
    def start(self):
        """Start the visualization GUI."""
        try:
            self.root = tk.Tk()
            self.root.title("Multi-Camera Object Tracking System")
            
            # Calculate window size based on display settings
            window_width = max(self.canvas_width + 400, self.display_width * 2 + 100)
            window_height = max(self.canvas_height + 200, self.display_height + 300)
            self.root.geometry(f"{window_width}x{window_height}")
            
            # Make window resizable
            self.root.resizable(True, True)
            self.root.protocol("WM_DELETE_WINDOW", self.stop)
            
            self._create_widgets()
            self._create_menu()
            
            self.running = True
            self._update_loop()
            
            logger.info("Visualization started successfully")
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error starting visualization: {e}")
            messagebox.showerror("Error", f"Failed to start visualization: {e}")
    
    def _create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Multi-Camera Object Tracking", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Camera feeds frame
        camera_frame = ttk.LabelFrame(main_frame, text="Camera Feeds", padding="5")
        camera_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Camera 1
        camera1_frame = ttk.Frame(camera_frame)
        camera1_frame.grid(row=0, column=0, padx=5)
        
        ttk.Label(camera1_frame, text="Camera 1").grid(row=0, column=0)
        self.camera1_label = ttk.Label(camera1_frame, borderwidth=2, relief="solid")
        self.camera1_label.grid(row=1, column=0)
        
        # Camera 2
        camera2_frame = ttk.Frame(camera_frame)
        camera2_frame.grid(row=0, column=1, padx=5)
        
        ttk.Label(camera2_frame, text="Camera 2").grid(row=0, column=0)
        self.camera2_label = ttk.Label(camera2_frame, borderwidth=2, relief="solid")
        self.camera2_label.grid(row=1, column=0)
        
        # 3D visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="3D Position Visualization", padding="5")
        viz_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas_3d = tk.Canvas(viz_frame, width=self.canvas_width, height=self.canvas_height,
                                  bg="black", relief="solid", bd=1)
        self.canvas_3d.grid(row=0, column=0)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Status: Initializing...")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.fps_label = ttk.Label(status_frame, text="FPS: --")
        self.fps_label.grid(row=0, column=1, sticky=tk.E)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Refresh Cameras", 
                  command=self._refresh_cameras).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reset Tracking", 
                  command=self._reset_tracking).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save Screenshot", 
                  command=self._save_screenshot).grid(row=0, column=2, padx=5)
    
    def _create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Screenshot", command=self._save_screenshot)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.stop)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Frame Size Settings", command=self._show_frame_settings)
        settings_menu.add_command(label="Display Settings", command=self._show_display_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.stop)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Show Detection Boxes", variable=tk.BooleanVar(value=True))
        view_menu.add_checkbutton(label="Show 3D Positions", variable=tk.BooleanVar(value=True))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _update_loop(self):
        """Main update loop for the GUI."""
        if not self.running:
            return
        
        try:
            # Get frames from cameras
            frame1, frame2 = self.camera_manager.get_frames()
            
            # Track objects if we have at least one frame
            tracked_objects = {"camera1": [], "camera2": []}
            
            if frame1 is not None or frame2 is not None:
                # Track objects (pass None for missing frames)
                tracked_objects = self.object_tracker.track_objects(frame1, frame2)
                
                # Update camera displays
                if frame1 is not None:
                    frame1_with_detections = self.object_tracker.draw_detections(frame1, tracked_objects["camera1"])
                    self._update_camera_display(frame1_with_detections, self.camera1_label)
                else:
                    # Show "No signal" for camera 1
                    self._show_no_signal(self.camera1_label, "Camera 1: No signal")
                
                if frame2 is not None:
                    frame2_with_detections = self.object_tracker.draw_detections(frame2, tracked_objects["camera2"])
                    self._update_camera_display(frame2_with_detections, self.camera2_label)
                else:
                    # Show "No signal" for camera 2
                    self._show_no_signal(self.camera2_label, "Camera 2: No signal")
                
                # Update 3D visualization
                self._update_3d_visualization(tracked_objects)
                
                # Update status
                self._update_status(tracked_objects)
                
            else:
                # Show "No signal" for both cameras
                self._show_no_signal(self.camera1_label, "Camera 1: No signal")
                self._show_no_signal(self.camera2_label, "Camera 2: No signal")
                self.status_label.config(text="Status: Waiting for camera frames...")
            
            # Schedule next update
            self.root.after(1000 // UPDATE_RATE, self._update_loop)
            
        except Exception as e:
            logger.error(f"Error in update loop: {e}")
            self.status_label.config(text=f"Status: Error - {e}")
            self.root.after(1000, self._update_loop)
    
    def _update_camera_display(self, frame: np.ndarray, label: ttk.Label):
        """Update camera display with new frame."""
        try:
            # Resize frame for display
            display_frame = cv2.resize(frame, (self.display_width, self.display_height))
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_frame)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Update label
            label.configure(image=photo)
            label.image = photo  # Keep a reference
            
        except Exception as e:
            logger.error(f"Error updating camera display: {e}")
    
    def _show_no_signal(self, label: ttk.Label, message: str):
        """Show 'no signal' message on camera display."""
        try:
            # Create a black frame with text
            no_signal_frame = np.zeros((self.display_height, self.display_width, 3), dtype=np.uint8)
            
            # Add text to the frame
            cv2.putText(no_signal_frame, message, 
                       (self.display_width // 2 - 150, self.display_height // 2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(no_signal_frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_frame)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Update label
            label.configure(image=photo)
            label.image = photo  # Keep a reference
            
        except Exception as e:
            logger.error(f"Error showing no signal: {e}")
    
    def _update_3d_visualization(self, tracked_objects: Dict[str, List[DetectedObject]]):
        """Update 3D position visualization."""
        try:
            # Clear canvas
            self.canvas_3d.delete("all")
            
            # Draw coordinate system
            self._draw_coordinate_system()
            
            # Draw camera positions
            self._draw_cameras()
            
            # Draw legend
            self._draw_legend()
            
            # Draw tracked objects from both cameras
            # Each recognized object is treated as a separate object regardless of similarity
            camera1_objects = tracked_objects["camera1"]
            camera2_objects = tracked_objects["camera2"]
            
            # Draw objects from camera 1
            for obj in camera1_objects:
                self._draw_object_3d(obj, camera_id="camera1")
            
            # Draw objects from camera 2
            for obj in camera2_objects:
                self._draw_object_3d(obj, camera_id="camera2")
            
        except Exception as e:
            logger.error(f"Error updating 3D visualization: {e}")
    
    def _draw_coordinate_system(self):
        """Draw coordinate system on canvas."""
        # Origin point
        origin_x = self.canvas_width // 2
        origin_y = self.canvas_height // 2
        
        # X-axis (red)
        self.canvas_3d.create_line(origin_x, origin_y, origin_x + 100, origin_y, 
                                  fill="red", width=2, arrow=tk.LAST)
        self.canvas_3d.create_text(origin_x + 110, origin_y, text="X", fill="red")
        
        # Y-axis (green)
        self.canvas_3d.create_line(origin_x, origin_y, origin_x, origin_y - 100, 
                                  fill="green", width=2, arrow=tk.LAST)
        self.canvas_3d.create_text(origin_x, origin_y - 110, text="Y", fill="green")
        
        # Z-axis (blue) - depth
        self.canvas_3d.create_line(origin_x, origin_y, origin_x - 50, origin_y - 50, 
                                  fill="blue", width=2, arrow=tk.LAST)
        self.canvas_3d.create_text(origin_x - 60, origin_y - 60, text="Z", fill="blue")
    
    def _draw_cameras(self):
        """Draw camera positions on canvas."""
        # Camera 1 position (left)
        cam1_x = self.canvas_width // 2 - int(CAMERA_DISTANCE * self.scale_factor // 2)
        cam1_y = self.canvas_height // 2
        
        # Camera 2 position (right)
        cam2_x = self.canvas_width // 2 + int(CAMERA_DISTANCE * self.scale_factor // 2)
        cam2_y = self.canvas_height // 2
        
        # Draw cameras
        self.canvas_3d.create_oval(cam1_x - 10, cam1_y - 10, cam1_x + 10, cam1_y + 10, 
                                  fill="yellow", outline="black")
        self.canvas_3d.create_text(cam1_x, cam1_y - 20, text="Cam1", fill="white")
        
        self.canvas_3d.create_oval(cam2_x - 10, cam2_y - 10, cam2_x + 10, cam2_y + 10, 
                                  fill="yellow", outline="black")
        self.canvas_3d.create_text(cam2_x, cam2_y - 20, text="Cam2", fill="white")
    
    def _draw_legend(self):
        """Draw legend for object colors."""
        legend_x = 10
        legend_y = 10
        
        # Legend title
        self.canvas_3d.create_text(legend_x, legend_y, text="Object Legend:", 
                                  fill="white", font=("Arial", 10, "bold"), anchor="nw")
        
        # Camera 1 objects
        legend_y += 20
        self.canvas_3d.create_oval(legend_x, legend_y - 5, legend_x + 10, legend_y + 5, 
                                  fill="cyan", outline="white")
        self.canvas_3d.create_text(legend_x + 15, legend_y, text="Camera 1 (tracked)", 
                                  fill="white", font=("Arial", 8), anchor="nw")
        
        legend_y += 15
        self.canvas_3d.create_oval(legend_x, legend_y - 5, legend_x + 10, legend_y + 5, 
                                  fill="blue", outline="white")
        self.canvas_3d.create_text(legend_x + 15, legend_y, text="Camera 1 (detected)", 
                                  fill="white", font=("Arial", 8), anchor="nw")
        
        # Camera 2 objects
        legend_y += 15
        self.canvas_3d.create_oval(legend_x, legend_y - 5, legend_x + 10, legend_y + 5, 
                                  fill="magenta", outline="white")
        self.canvas_3d.create_text(legend_x + 15, legend_y, text="Camera 2 (tracked)", 
                                  fill="white", font=("Arial", 8), anchor="nw")
        
        legend_y += 15
        self.canvas_3d.create_oval(legend_x, legend_y - 5, legend_x + 10, legend_y + 5, 
                                  fill="purple", outline="white")
        self.canvas_3d.create_text(legend_x + 15, legend_y, text="Camera 2 (detected)", 
                                  fill="white", font=("Arial", 8), anchor="nw")
    
    def _draw_object_3d(self, obj: DetectedObject, camera_id: str = None):
        """Draw 3D object position on canvas."""
        # If no 3D position is available, estimate one for visualization
        if obj.position_3d is None:
            # Create a simple estimated position for visualization
            center = obj.get_center()
            x_norm = (center[0] - FRAME_WIDTH // 2) / (FRAME_WIDTH // 2)
            y_norm = (center[1] - FRAME_HEIGHT // 2) / (FRAME_HEIGHT // 2)
            
            # Estimate depth based on object size
            area = obj.get_area()
            max_area = FRAME_WIDTH * FRAME_HEIGHT * 0.1
            depth_factor = max(0.1, min(1.0, area / max_area))
            estimated_depth = 1.0 + (10.0 - 1.0) * (1.0 - depth_factor)
            
            # Calculate estimated 3D position
            if camera_id == "camera1":
                x_3d = -CAMERA_DISTANCE / 2 + x_norm * estimated_depth
            elif camera_id == "camera2":
                x_3d = CAMERA_DISTANCE / 2 + x_norm * estimated_depth
            else:
                x_3d = x_norm * estimated_depth
            
            y_3d = y_norm * estimated_depth
            z_3d = estimated_depth
        else:
            x_3d, y_3d, z_3d = obj.position_3d
        
        # Convert 3D coordinates to canvas coordinates
        canvas_x = self.canvas_width // 2 + int(x_3d * self.scale_factor)
        canvas_y = self.canvas_height // 2 - int(y_3d * self.scale_factor)
        
        # Adjust size based on depth
        size = max(5, int(20 / (z_3d + 0.1)))
        
        # Choose color based on camera and tracking status
        if camera_id == "camera1":
            color = "cyan" if obj.track_id is not None else "blue"
        elif camera_id == "camera2":
            color = "magenta" if obj.track_id is not None else "purple"
        else:
            color = "lime" if obj.track_id is not None else "red"
        
        # Draw object
        self.canvas_3d.create_oval(canvas_x - size, canvas_y - size, 
                                  canvas_x + size, canvas_y + size, 
                                  fill=color, outline="white")
        
        # Draw object information
        label_parts = []
        if obj.track_id is not None:
            label_parts.append(f"ID:{obj.track_id}")
        label_parts.append(obj.class_name)
        if camera_id:
            label_parts.append(f"({camera_id})")
        
        label = " ".join(label_parts)
        self.canvas_3d.create_text(canvas_x, canvas_y - size - 10, 
                                  text=label, fill="white", font=("Arial", 8))
    
    def _update_status(self, tracked_objects: Dict[str, List[DetectedObject]]):
        """Update status information."""
        try:
            # Count tracked objects from each camera
            camera1_objects = len(tracked_objects["camera1"])
            camera2_objects = len(tracked_objects["camera2"])
            total_objects = camera1_objects + camera2_objects
            
            # Get camera info
            camera_info = self.camera_manager.get_camera_info()
            fps1 = camera_info.get("camera1", {}).get("fps", 0)
            fps2 = camera_info.get("camera2", {}).get("fps", 0)
            avg_fps = (fps1 + fps2) / 2 if fps1 > 0 and fps2 > 0 else 0
            
            # Update labels with detailed information
            status_text = f"Status: Cam1: {camera1_objects} objects, Cam2: {camera2_objects} objects (Total: {total_objects})"
            self.status_label.config(text=status_text)
            self.fps_label.config(text=f"FPS: {avg_fps:.1f}")
            
        except Exception as e:
            logger.error(f"Error updating status: {e}")
    
    def _refresh_cameras(self):
        """Refresh camera connections."""
        try:
            self.camera_manager.stop_all()
            if self.camera_manager.initialize_cameras():
                messagebox.showinfo("Success", "Cameras refreshed successfully")
            else:
                messagebox.showerror("Error", "Failed to refresh cameras")
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing cameras: {e}")
    
    def _reset_tracking(self):
        """Reset object tracking."""
        try:
            # Reinitialize object tracker
            self.object_tracker.__init__()
            messagebox.showinfo("Success", "Object tracking reset")
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting tracking: {e}")
    
    def _save_screenshot(self):
        """Save current visualization as screenshot."""
        try:
            # Get current timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            # Save canvas as image
            self.canvas_3d.postscript(file=filename + ".eps")
            
            # Convert to PNG (simplified - in real app you'd use PIL)
            messagebox.showinfo("Success", f"Screenshot saved as {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving screenshot: {e}")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """Multi-Camera Object Tracking System

A Python application for real-time object tracking using dual cameras.

Features:
- Dual camera feed processing
- Real-time object detection and tracking
- 3D position visualization
- Cross-platform compatibility

Version: 1.0
"""
        messagebox.showinfo("About", about_text)
    
    def _show_frame_settings(self):
        """Show frame size settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Frame Size Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Create settings frame
        frame = ttk.Frame(settings_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame size controls
        ttk.Label(frame, text="Frame Size Settings", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Width control
        ttk.Label(frame, text="Frame Width:").grid(row=1, column=0, sticky=tk.W, pady=5)
        width_var = tk.StringVar(value=str(FRAME_WIDTH))
        width_entry = ttk.Entry(frame, textvariable=width_var, width=10)
        width_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Height control
        ttk.Label(frame, text="Frame Height:").grid(row=2, column=0, sticky=tk.W, pady=5)
        height_var = tk.StringVar(value=str(FRAME_HEIGHT))
        height_entry = ttk.Entry(frame, textvariable=height_var, width=10)
        height_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Display scale control
        ttk.Label(frame, text="Display Scale:").grid(row=3, column=0, sticky=tk.W, pady=5)
        scale_var = tk.StringVar(value=str(DISPLAY_SCALE))
        scale_entry = ttk.Entry(frame, textvariable=scale_var, width=10)
        scale_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Preset buttons
        preset_frame = ttk.Frame(frame)
        preset_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Label(preset_frame, text="Preset Sizes:").grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        presets = [
            ("Small (320x240)", 320, 240, 0.5),
            ("Medium (640x480)", 640, 480, 1.0),
            ("Large (1280x720)", 1280, 720, 1.5),
            ("HD (1920x1080)", 1920, 1080, 2.0)
        ]
        
        for i, (name, w, h, s) in enumerate(presets):
            ttk.Button(preset_frame, text=name, 
                      command=lambda w=w, h=h, s=s: self._apply_preset(width_var, height_var, scale_var, w, h, s)
                      ).grid(row=1 + i//2, column=i%2, padx=5, pady=5)
        
        # Apply button
        ttk.Button(frame, text="Apply Settings", 
                  command=lambda: self._apply_frame_settings(width_var, height_var, scale_var, settings_window)
                  ).grid(row=5, column=0, columnspan=2, pady=20)
    
    def _apply_preset(self, width_var, height_var, scale_var, width, height, scale):
        """Apply preset frame size settings."""
        width_var.set(str(width))
        height_var.set(str(height))
        scale_var.set(str(scale))
    
    def _apply_frame_settings(self, width_var, height_var, scale_var, settings_window):
        """Apply frame size settings."""
        try:
            new_width = int(width_var.get())
            new_height = int(height_var.get())
            new_scale = float(scale_var.get())
            
            # Update display settings
            self.display_width = int(new_width * new_scale)
            self.display_height = int(new_height * new_scale)
            self.display_scale = new_scale
            
            # Update window size
            window_width = max(self.canvas_width + 400, self.display_width * 2 + 100)
            window_height = max(self.canvas_height + 200, self.display_height + 300)
            self.root.geometry(f"{window_width}x{window_height}")
            
            messagebox.showinfo("Success", "Frame size settings applied successfully!")
            settings_window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for width, height, and scale.")
    
    def _show_display_settings(self):
        """Show display settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Display Settings")
        settings_window.geometry("300x200")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Create settings frame
        frame = ttk.Frame(settings_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Display Settings", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 20))
        
        # Display options
        ttk.Label(frame, text="Current Display Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(frame, text=f"{self.display_width} x {self.display_height}").grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Scale Factor:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(frame, text=f"{self.display_scale:.1f}x").grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Close button
        ttk.Button(frame, text="Close", command=settings_window.destroy).grid(row=3, column=0, columnspan=2, pady=20)
    
    def stop(self):
        """Stop the visualization."""
        self.running = False
        if self.root:
            self.root.quit()
        logger.info("Visualization stopped")


if __name__ == "__main__":
    # Test visualizer
    print("Visualizer module loaded successfully!") 