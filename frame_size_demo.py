"""
Demo script for frame size configuration features
"""

import cv2
import numpy as np
from config import *

def demo_frame_size_configuration():
    """Demonstrate frame size configuration features."""
    
    print("🎥 Frame Size Configuration Demo")
    print("=" * 50)
    print("This demo shows how to configure frame sizes to prevent cropping.")
    print()
    
    # Show current configuration
    print("📋 Current Configuration:")
    print(f"  Frame Width: {FRAME_WIDTH}")
    print(f"  Frame Height: {FRAME_HEIGHT}")
    print(f"  Display Width: {DISPLAY_WIDTH}")
    print(f"  Display Height: {DISPLAY_HEIGHT}")
    print(f"  Display Scale: {DISPLAY_SCALE}")
    print()
    
    # Show different configuration options
    print("⚙️ Configuration Options:")
    print()
    
    configurations = [
        {
            'name': 'Small (Good for performance)',
            'frame_width': 320,
            'frame_height': 240,
            'display_scale': 0.5,
            'description': 'Small frames, fast processing'
        },
        {
            'name': 'Medium (Balanced)',
            'frame_width': 640,
            'frame_height': 480,
            'display_scale': 1.0,
            'description': 'Standard size, good balance'
        },
        {
            'name': 'Large (High quality)',
            'frame_width': 1280,
            'frame_height': 720,
            'display_scale': 1.5,
            'description': 'High quality, larger display'
        },
        {
            'name': 'HD (Maximum quality)',
            'frame_width': 1920,
            'frame_height': 1080,
            'display_scale': 2.0,
            'description': 'Maximum quality, large display'
        }
    ]
    
    for i, config in enumerate(configurations, 1):
        display_width = int(config['frame_width'] * config['display_scale'])
        display_height = int(config['frame_height'] * config['display_scale'])
        window_width = max(800 + 400, display_width * 2 + 100)
        window_height = max(600 + 200, display_height + 300)
        
        print(f"{i}. {config['name']}")
        print(f"   Frame: {config['frame_width']}x{config['frame_height']}")
        print(f"   Display: {display_width}x{display_height}")
        print(f"   Window: {window_width}x{window_height}")
        print(f"   Description: {config['description']}")
        print()
    
    print("🔧 How to Change Frame Sizes:")
    print()
    print("Method 1: Edit config.py")
    print("  FRAME_WIDTH = 640")
    print("  FRAME_HEIGHT = 480")
    print("  DISPLAY_SCALE = 1.0")
    print()
    print("Method 2: Use GUI Settings")
    print("  Settings → Frame Size Settings")
    print("  Choose from presets or enter custom values")
    print()
    print("Method 3: Runtime Configuration")
    print("  The GUI allows changing display scale without restarting")
    print()
    
    print("💡 Tips to Prevent Cropping:")
    print("1. Set DISPLAY_SCALE to 1.0 or higher")
    print("2. Ensure window size accommodates frame size")
    print("3. Use the GUI settings to preview changes")
    print("4. Test with your specific camera setup")
    print()
    
    print("🚀 Quick Start:")
    print("1. Run the main application: python main.py")
    print("2. Go to Settings → Frame Size Settings")
    print("3. Choose a preset or enter custom values")
    print("4. Click 'Apply Settings'")
    print("5. The window will resize automatically")
    print()
    
    print("✅ Benefits of the New System:")
    print("- Configurable frame sizes")
    print("- Automatic window sizing")
    print("- Real-time display scale adjustment")
    print("- Preset configurations")
    print("- No more cropped frames!")

def show_configuration_examples():
    """Show example configurations for different use cases."""
    
    print("\n📝 Configuration Examples for Different Use Cases:")
    print("=" * 60)
    
    examples = [
        {
            'use_case': 'Performance Testing',
            'frame_width': 320,
            'frame_height': 240,
            'display_scale': 0.5,
            'reason': 'Small frames for maximum speed'
        },
        {
            'use_case': 'Development/Debugging',
            'frame_width': 640,
            'frame_height': 480,
            'display_scale': 1.0,
            'reason': 'Standard size, easy to work with'
        },
        {
            'use_case': 'Quality Testing',
            'frame_width': 1280,
            'frame_height': 720,
            'display_scale': 1.5,
            'reason': 'High quality for detailed analysis'
        },
        {
            'use_case': 'Presentation/Demo',
            'frame_width': 1920,
            'frame_height': 1080,
            'display_scale': 2.0,
            'reason': 'Maximum quality for presentations'
        }
    ]
    
    for example in examples:
        display_width = int(example['frame_width'] * example['display_scale'])
        display_height = int(example['frame_height'] * example['display_scale'])
        
        print(f"\n🎯 {example['use_case']}:")
        print(f"   Frame: {example['frame_width']}x{example['frame_height']}")
        print(f"   Display: {display_width}x{display_height}")
        print(f"   Reason: {example['reason']}")
        print(f"   Config: FRAME_WIDTH={example['frame_width']}, FRAME_HEIGHT={example['frame_height']}, DISPLAY_SCALE={example['display_scale']}")

if __name__ == "__main__":
    demo_frame_size_configuration()
    show_configuration_examples()
    print("\n🎉 Frame size configuration demo completed!")
    print("\nTo test the new features, run: python main.py") 