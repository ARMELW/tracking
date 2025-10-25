#!/usr/bin/env python3
"""
Screen Recorder Demo
Demonstrates the screen recorder functionality with a simulated screen.
"""

import cv2
import numpy as np
from screen_recorder import ScreenRecorder
import time


def create_demo_screen(width=800, height=600, frame_number=0):
    """
    Create a demo screen with animated content.
    
    Args:
        width: Screen width
        height: Screen height
        frame_number: Current frame number for animation
    
    Returns:
        Demo screen image
    """
    # Create blank canvas
    screen = np.ones((height, width, 3), dtype=np.uint8) * 240
    
    # Add title
    cv2.putText(screen, "Screen Recorder Demo", (width//2 - 200, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    
    # Add animated circle
    t = frame_number * 0.1
    circle_x = int(width // 2 + 150 * np.cos(t))
    circle_y = int(height // 2 + 100 * np.sin(t))
    cv2.circle(screen, (circle_x, circle_y), 30, (255, 0, 0), -1)
    
    # Add animated rectangle
    rect_x = int(width // 4 + 100 * np.sin(t))
    rect_y = int(height // 2)
    cv2.rectangle(screen, (rect_x - 40, rect_y - 40), (rect_x + 40, rect_y + 40), (0, 255, 0), -1)
    
    # Add frame counter
    cv2.putText(screen, f"Frame: {frame_number}", (20, height - 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Add instructions
    instructions = [
        "This is a demo of the screen recorder",
        "The shapes are animated for demonstration",
        "Use the screen recorder to capture this window"
    ]
    
    y_offset = height // 2 + 100
    for i, instruction in enumerate(instructions):
        cv2.putText(screen, instruction, (width // 2 - 250, y_offset + i * 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    
    return screen


def run_demo():
    """Run the screen recorder demo with simulated content."""
    print("=" * 60)
    print("  Screen Recorder Demo")
    print("=" * 60)
    print()
    print("This demo shows animated content that you can record.")
    print()
    print("Instructions:")
    print("1. This window will display animated shapes")
    print("2. Run screen_recorder.py in another terminal")
    print("3. Select this demo window region to record")
    print("4. Press SPACE in the recorder to start/stop recording")
    print("5. Press Q in the recorder to save and exit")
    print()
    print("Press Q in this window to close the demo")
    print()
    
    window_name = "Demo Content - Record This Window"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    frame_number = 0
    
    try:
        while True:
            # Create demo screen
            screen = create_demo_screen(frame_number=frame_number)
            
            # Display
            cv2.imshow(window_name, screen)
            
            # Handle keyboard input
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('q'):
                print("Demo closed")
                break
            
            frame_number += 1
            
    except KeyboardInterrupt:
        print("\nDemo interrupted")
    finally:
        cv2.destroyAllWindows()


def main():
    """Main entry point."""
    run_demo()


if __name__ == "__main__":
    main()
