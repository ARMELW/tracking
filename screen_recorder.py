#!/usr/bin/env python3
"""
Screen Recorder
Records a selected region of the screen and exports as MP4 video.
"""

import cv2
import numpy as np
import mss
import time
import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class ScreenRecorder:
    """Record screen region and export as MP4 video."""
    
    def __init__(self, output_path: str = None, fps: int = 30, 
                 codec: str = "mp4v", screen_region: Optional[Dict] = None):
        """
        Initialize the screen recorder.
        
        Args:
            output_path: Path for the output video file (default: screen_recording_TIMESTAMP.mp4)
            fps: Frames per second for recording (default: 30)
            codec: Video codec to use (default: 'mp4v' for MP4)
            screen_region: Dictionary with 'top', 'left', 'width', 'height' for screen capture.
                          If None, user will select region.
        """
        self.screen_region = screen_region
        self.fps = fps
        self.codec = codec
        self.sct = None  # Lazy initialization
        self.video_writer = None
        self.is_recording = False
        self.frames_recorded = 0
        self.recording_start_time = None
        
        # Set output path
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_path = f"screen_recording_{timestamp}.mp4"
        else:
            self.output_path = output_path
        
        # Ensure output path has .mp4 extension
        if not self.output_path.lower().endswith('.mp4'):
            self.output_path += '.mp4'
    
    def select_screen_region(self) -> Dict:
        """
        Allow user to select screen region to capture.
        Returns dictionary with screen region coordinates.
        """
        print("Select the screen region to record:")
        print("  - Click and drag to select the area")
        print("  - Press ENTER to confirm selection")
        print("  - Press ESC to cancel")
        
        # Initialize mss if not already done
        if self.sct is None:
            self.sct = mss.mss()
        
        # Capture full screen first
        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Let user select region
        roi = cv2.selectROI("Select Screen Region to Record", img, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Screen Region to Record")
        
        if roi[2] > 0 and roi[3] > 0:
            region = {
                "top": monitor["top"] + int(roi[1]),
                "left": monitor["left"] + int(roi[0]),
                "width": int(roi[2]),
                "height": int(roi[3])
            }
            print(f"Selected region: {region['width']}x{region['height']} at ({region['left']}, {region['top']})")
            return region
        return None
    
    def capture_frame(self) -> np.ndarray:
        """Capture a frame from the selected screen region."""
        if self.screen_region is None:
            self.screen_region = self.select_screen_region()
            if self.screen_region is None:
                raise ValueError("No screen region selected")
        
        # Initialize mss if not already done
        if self.sct is None:
            self.sct = mss.mss()
        
        screenshot = self.sct.grab(self.screen_region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame
    
    def start_recording(self):
        """Start recording video."""
        if self.is_recording:
            print("Already recording!")
            return
        
        # Ensure we have a screen region
        if self.screen_region is None:
            self.screen_region = self.select_screen_region()
            if self.screen_region is None:
                raise ValueError("No screen region selected")
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        width = self.screen_region['width']
        height = self.screen_region['height']
        
        self.video_writer = cv2.VideoWriter(
            self.output_path,
            fourcc,
            self.fps,
            (width, height)
        )
        
        if not self.video_writer.isOpened():
            raise RuntimeError("Failed to initialize video writer")
        
        self.is_recording = True
        self.frames_recorded = 0
        self.recording_start_time = time.time()
        print(f"Recording started: {self.output_path}")
    
    def stop_recording(self):
        """Stop recording and save video."""
        if not self.is_recording:
            print("Not currently recording!")
            return
        
        self.is_recording = False
        
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        
        duration = time.time() - self.recording_start_time if self.recording_start_time else 0
        print(f"\nRecording stopped!")
        print(f"  Frames recorded: {self.frames_recorded}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  Video saved to: {os.path.abspath(self.output_path)}")
    
    def record_frame(self, frame: np.ndarray):
        """Record a single frame to the video."""
        if self.is_recording and self.video_writer is not None:
            self.video_writer.write(frame)
            self.frames_recorded += 1
    
    def annotate_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Annotate the frame with recording status and controls.
        
        Args:
            frame: Input frame
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        # Recording indicator
        if self.is_recording:
            # Red recording dot
            cv2.circle(annotated, (20, 20), 10, (0, 0, 255), -1)
            
            # Recording text
            cv2.putText(annotated, "REC", (40, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Frame counter
            duration = time.time() - self.recording_start_time if self.recording_start_time else 0
            text = f"Time: {duration:.1f}s | Frames: {self.frames_recorded}"
            cv2.putText(annotated, text, (100, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            # Ready to record indicator
            cv2.putText(annotated, "Ready", (20, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display instructions at the bottom
        instructions = [
            "SPACE: Start/Stop Recording",
            "Q: Quit and Export",
            "ESC: Cancel and Quit"
        ]
        
        y_offset = frame.shape[0] - 15 - (len(instructions) * 25)
        for i, instruction in enumerate(instructions):
            cv2.putText(annotated, instruction, (10, y_offset + i * 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated
    
    def run(self):
        """Main loop to run the screen recorder."""
        print("=" * 60)
        print("  Screen Recorder")
        print("=" * 60)
        print()
        print("Controls:")
        print("  SPACE: Start/Stop recording")
        print("  Q: Quit and export video")
        print("  ESC: Cancel and quit without saving")
        print()
        
        try:
            # Create window that stays on top
            window_name = "Screen Recorder"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # Calculate wait time for cv2.waitKey based on FPS
            wait_time = int(1000.0 / self.fps)  # milliseconds
            
            while True:
                # Track timing for accurate frame rate
                loop_start = time.time()
                
                # Capture frame
                frame = self.capture_frame()
                
                # Record if recording is active
                if self.is_recording:
                    self.record_frame(frame)
                
                # Annotate frame
                annotated = self.annotate_frame(frame)
                
                # Display
                cv2.imshow(window_name, annotated)
                
                # Handle keyboard input with frame-rate-appropriate timeout
                key = cv2.waitKey(wait_time) & 0xFF
                
                if key == ord('q'):
                    # Stop recording if active and quit
                    if self.is_recording:
                        self.stop_recording()
                    print("Exiting...")
                    break
                elif key == 27:  # ESC key
                    # Cancel recording and quit
                    if self.is_recording:
                        self.is_recording = False
                        if self.video_writer is not None:
                            self.video_writer.release()
                            self.video_writer = None
                        # Remove the incomplete video file
                        if os.path.exists(self.output_path):
                            os.remove(self.output_path)
                        print("Recording cancelled")
                    print("Exiting without saving...")
                    break
                elif key == 32:  # SPACE key
                    if self.is_recording:
                        self.stop_recording()
                    else:
                        self.start_recording()
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            if self.is_recording:
                self.stop_recording()
        finally:
            if self.video_writer is not None:
                self.video_writer.release()
            cv2.destroyAllWindows()


def main():
    """Command-line interface for screen recorder."""
    parser = argparse.ArgumentParser(
        description="Record a selected region of the screen and export as MP4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start screen recorder (select region interactively)
  python screen_recorder.py
  
  # Record with custom output file
  python screen_recorder.py -o my_recording.mp4
  
  # Record at 60 FPS
  python screen_recorder.py --fps 60
  
  # Record with custom codec
  python screen_recorder.py --codec avc1

Controls during recording:
  SPACE: Start/Stop recording
  Q: Quit and export video
  ESC: Cancel and quit without saving
        """
    )
    
    parser.add_argument("-o", "--output", help="Output video file path (default: screen_recording_TIMESTAMP.mp4)")
    parser.add_argument("--fps", type=int, default=30,
                       help="Frames per second for recording (default: 30)")
    parser.add_argument("--codec", default="mp4v",
                       help="Video codec to use (default: mp4v)")
    
    args = parser.parse_args()
    
    try:
        # Create recorder
        recorder = ScreenRecorder(
            output_path=args.output,
            fps=args.fps,
            codec=args.codec
        )
        
        # Run the recorder
        recorder.run()
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
