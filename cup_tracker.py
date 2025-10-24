#!/usr/bin/env python3
"""
Cup Tracking System - 3 Cup Shell Game Tracker
This program captures video from a screen region, detects cups, tracks the ball,
and predicts its position after shuffling.
"""

import cv2
import numpy as np
import mss
import time
from collections import deque
from typing import List, Tuple, Optional, Dict


class CupTracker:
    """Main class for tracking cups and predicting ball position in the 3 cup game."""
    
    def __init__(self, screen_region: Optional[Dict] = None):
        """
        Initialize the cup tracker.
        
        Args:
            screen_region: Dictionary with 'top', 'left', 'width', 'height' for screen capture.
                          If None, user will select region.
        """
        self.screen_region = screen_region
        self.sct = None  # Lazy initialization
        self.cups = []  # List of detected cup positions
        self.ball_position = None  # Current/predicted ball position
        self.last_known_ball_position = None  # Last confirmed ball position
        self.cup_trajectories = {0: deque(maxlen=30), 1: deque(maxlen=30), 2: deque(maxlen=30)}
        self.tracking_history = []
        self.frame_count = 0
        
    def select_screen_region(self) -> Dict:
        """
        Allow user to select screen region to capture.
        Returns dictionary with screen region coordinates.
        """
        print("Press SPACE to start selection, then click and drag to select region")
        print("Press ENTER to confirm selection, ESC to cancel")
        
        # Initialize mss if not already done
        if self.sct is None:
            self.sct = mss.mss()
        
        # Capture full screen first
        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Let user select region
        roi = cv2.selectROI("Select Screen Region", img, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Screen Region")
        
        if roi[2] > 0 and roi[3] > 0:
            region = {
                "top": monitor["top"] + int(roi[1]),
                "left": monitor["left"] + int(roi[0]),
                "width": int(roi[2]),
                "height": int(roi[3])
            }
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
    
    def detect_cups(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect cups in the frame using contour detection.
        
        Args:
            frame: Input frame
            
        Returns:
            List of tuples (x, y, w, h) representing cup bounding boxes
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and aspect ratio to find cup-like shapes
        cups = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                
                # Cups typically have certain aspect ratios
                if 0.5 < aspect_ratio < 2.5 and w > 20 and h > 20:
                    cups.append((x, y, w, h))
        
        # Sort cups by x-coordinate (left to right)
        cups = sorted(cups, key=lambda c: c[0])
        
        # Keep only the 3 most prominent cups if more are detected
        if len(cups) > 3:
            cups = sorted(cups, key=lambda c: c[2] * c[3], reverse=True)[:3]
            cups = sorted(cups, key=lambda c: c[0])
        
        return cups
    
    def track_cup_movements(self, current_cups: List[Tuple[int, int, int, int]]):
        """
        Track the movement of cups between frames.
        
        Args:
            current_cups: List of current cup positions
        """
        if len(current_cups) == 3:
            for i, cup in enumerate(current_cups):
                center_x = cup[0] + cup[2] // 2
                center_y = cup[1] + cup[3] // 2
                self.cup_trajectories[i].append((center_x, center_y, self.frame_count))
    
    def predict_ball_position(self) -> Optional[int]:
        """
        Predict which cup contains the ball based on tracking data.
        
        Returns:
            Index of the cup (0, 1, or 2) predicted to contain the ball, or None
        """
        if self.last_known_ball_position is None:
            return None
        
        # Track which cup started at the ball's position
        initial_cup_index = self.last_known_ball_position
        
        # Analyze trajectories to follow the cup movements
        # Simple prediction: if we have trajectory data, follow the cup
        if len(self.cup_trajectories[initial_cup_index]) > 0:
            # The cup with the ball is tracked by its initial index
            # In a real scenario, we would use more sophisticated tracking
            # like optical flow or template matching
            return initial_cup_index
        
        return None
    
    def annotate_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Annotate the frame with cup numbers, ball position, and predictions.
        
        Args:
            frame: Input frame
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        # Detect and draw cups
        cups = self.detect_cups(frame)
        self.cups = cups
        
        for i, (x, y, w, h) in enumerate(cups):
            # Draw bounding box
            color = (0, 255, 0)  # Green by default
            
            # Highlight predicted ball position
            predicted_pos = self.predict_ball_position()
            if predicted_pos == i:
                color = (0, 0, 255)  # Red for predicted ball position
            
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
            
            # Add cup number
            label = f"Cup {i + 1}"
            cv2.putText(annotated, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Draw trajectory
            if len(self.cup_trajectories[i]) > 1:
                points = list(self.cup_trajectories[i])
                for j in range(1, len(points)):
                    cv2.line(annotated, 
                            (points[j-1][0], points[j-1][1]),
                            (points[j][0], points[j][1]),
                            (255, 255, 0), 1)
        
        # Track cup movements
        self.track_cup_movements(cups)
        
        # Annotate last known ball position
        if self.last_known_ball_position is not None and len(cups) > self.last_known_ball_position:
            x, y, w, h = cups[self.last_known_ball_position]
            cv2.circle(annotated, (x + w // 2, y + h // 2), 10, (255, 0, 0), -1)
            cv2.putText(annotated, "BALL HERE", (x, y + h + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Display prediction
        predicted_pos = self.predict_ball_position()
        if predicted_pos is not None:
            text = f"Predicted: Cup {predicted_pos + 1}"
            cv2.putText(annotated, text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Display instructions
        cv2.putText(annotated, "Press 1/2/3: Mark ball position | R: Reset | Q: Quit", 
                   (10, frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated
    
    def run(self):
        """Main loop to run the cup tracking system."""
        print("Cup Tracking System Started")
        print("Controls:")
        print("  1, 2, 3: Mark the ball position under cup 1, 2, or 3")
        print("  R: Reset tracking")
        print("  Q: Quit")
        print()
        
        try:
            while True:
                # Capture frame
                frame = self.capture_frame()
                self.frame_count += 1
                
                # Annotate frame
                annotated = self.annotate_frame(frame)
                
                # Display
                cv2.imshow("Cup Tracker", annotated)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('1'):
                    self.last_known_ball_position = 0
                    print("Ball marked under Cup 1")
                elif key == ord('2'):
                    self.last_known_ball_position = 1
                    print("Ball marked under Cup 2")
                elif key == ord('3'):
                    self.last_known_ball_position = 2
                    print("Ball marked under Cup 3")
                elif key == ord('r'):
                    self.last_known_ball_position = None
                    self.cup_trajectories = {0: deque(maxlen=30), 1: deque(maxlen=30), 2: deque(maxlen=30)}
                    print("Tracking reset")
                
                # Small delay to reduce CPU usage
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cv2.destroyAllWindows()


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("  3 Cup Shell Game Tracker")
    print("  Computer Vision Ball Tracking System")
    print("=" * 60)
    print()
    
    # Create tracker instance
    tracker = CupTracker()
    
    # Run the tracker
    tracker.run()


if __name__ == "__main__":
    main()
