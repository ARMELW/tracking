#!/usr/bin/env python3
"""
Advanced Cup Tracker with Template Matching
Improved tracking using template matching and color-based detection.
"""

import cv2
import numpy as np
import mss
from typing import List, Tuple, Optional, Dict
from collections import deque


class AdvancedCupTracker:
    """Advanced cup tracking with template matching and color detection."""
    
    def __init__(self, screen_region: Optional[Dict] = None):
        """Initialize the advanced tracker."""
        self.screen_region = screen_region
        self.sct = None  # Lazy initialization
        
        # Tracking state
        self.cup_templates = []
        self.cup_positions = []
        self.ball_cup_index = None
        self.prev_frame = None
        
        # Tracking history
        self.position_history = {0: deque(maxlen=50), 1: deque(maxlen=50), 2: deque(maxlen=50)}
        self.frame_count = 0
        
        # Colors for visualization
        self.colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        
    def select_screen_region(self) -> Dict:
        """Allow user to select screen region."""
        print("Select the screen region containing the cups...")
        
        # Initialize mss if not already done
        if self.sct is None:
            self.sct = mss.mss()
        
        monitor = self.sct.monitors[1]
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        roi = cv2.selectROI("Select Screen Region", img, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Screen Region")
        
        if roi[2] > 0 and roi[3] > 0:
            return {
                "top": monitor["top"] + int(roi[1]),
                "left": monitor["left"] + int(roi[0]),
                "width": int(roi[2]),
                "height": int(roi[3])
            }
        return None
    
    def capture_frame(self) -> np.ndarray:
        """Capture frame from screen region."""
        if self.screen_region is None:
            self.screen_region = self.select_screen_region()
            if self.screen_region is None:
                raise ValueError("No region selected")
        
        # Initialize mss if not already done
        if self.sct is None:
            self.sct = mss.mss()
        
        screenshot = self.sct.grab(self.screen_region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame
    
    def detect_cups_color(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect cups using color-based segmentation.
        Assumes cups are distinct from background.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for potential cup colors (adjust based on actual cup colors)
        # This is a general approach - may need tuning
        lower_bound = np.array([0, 0, 50])
        upper_bound = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        
        # Morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cups = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum area
                x, y, w, h = cv2.boundingRect(contour)
                if w > 30 and h > 30:  # Minimum dimensions
                    cups.append((x, y, w, h))
        
        # Sort and limit to 3 cups
        cups = sorted(cups, key=lambda c: c[0])
        if len(cups) > 3:
            cups = sorted(cups, key=lambda c: c[2] * c[3], reverse=True)[:3]
            cups = sorted(cups, key=lambda c: c[0])
        
        return cups
    
    def track_with_optical_flow(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Track cups using optical flow between frames.
        """
        if self.prev_frame is None or len(self.cup_positions) == 0:
            return self.detect_cups_color(frame)
        
        # Convert to grayscale
        gray_prev = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
        gray_curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow for cup centers
        updated_positions = []
        
        for x, y, w, h in self.cup_positions:
            # Get center point
            center = np.array([[[x + w // 2, y + h // 2]]], dtype=np.float32)
            
            # Calculate optical flow
            new_center, status, _ = cv2.calcOpticalFlowPyrLK(
                gray_prev, gray_curr, center, None,
                winSize=(15, 15),
                maxLevel=2,
                criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
            )
            
            if status[0][0] == 1:
                new_x = int(new_center[0][0][0] - w // 2)
                new_y = int(new_center[0][0][1] - h // 2)
                updated_positions.append((new_x, new_y, w, h))
            else:
                updated_positions.append((x, y, w, h))
        
        return updated_positions
    
    def update_tracking(self, cups: List[Tuple[int, int, int, int]]):
        """Update tracking history for each cup."""
        if len(cups) == 3:
            for i, (x, y, w, h) in enumerate(cups):
                center_x = x + w // 2
                center_y = y + h // 2
                self.position_history[i].append((center_x, center_y))
    
    def predict_ball_position(self) -> Optional[int]:
        """Predict ball position based on tracking."""
        if self.ball_cup_index is None:
            return None
        
        # Simple tracking: follow the cup index
        # In a more advanced system, we would use motion analysis
        # to determine if cups were swapped
        return self.ball_cup_index
    
    def draw_annotations(self, frame: np.ndarray, cups: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Draw all annotations on the frame."""
        annotated = frame.copy()
        
        for i, (x, y, w, h) in enumerate(cups):
            # Choose color
            color = self.colors[i % 3]
            
            # Highlight ball position
            if i == self.ball_cup_index:
                cv2.rectangle(annotated, (x-5, y-5), (x+w+5, y+h+5), (0, 255, 255), 3)
            
            # Draw cup rectangle
            cv2.rectangle(annotated, (x, y), (x+w, y+h), color, 2)
            
            # Cup number
            cv2.putText(annotated, f"#{i+1}", (x+w//2-10, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            # Draw trajectory
            if len(self.position_history[i]) > 1:
                points = list(self.position_history[i])
                for j in range(1, len(points)):
                    cv2.line(annotated, points[j-1], points[j], color, 2)
        
        # Show ball prediction
        predicted = self.predict_ball_position()
        if predicted is not None:
            cv2.putText(annotated, f"Ball -> Cup #{predicted+1}", (10, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            
            # Draw indicator at predicted cup
            if len(cups) > predicted:
                x, y, w, h = cups[predicted]
                cv2.circle(annotated, (x+w//2, y+h//2), 15, (0, 255, 255), 3)
        
        # Last known position
        if self.ball_cup_index is not None and len(cups) > self.ball_cup_index:
            x, y, w, h = cups[self.ball_cup_index]
            cv2.putText(annotated, "BALL", (x+w//2-20, y+h+30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Instructions
        cv2.putText(annotated, "Controls: 1/2/3=Mark Ball | R=Reset | Q=Quit",
                   (10, frame.shape[0]-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated
    
    def run(self):
        """Main tracking loop."""
        print("Advanced Cup Tracker Started")
        print("Controls:")
        print("  1, 2, 3: Mark ball under cup 1, 2, or 3")
        print("  R: Reset")
        print("  Q: Quit")
        
        try:
            while True:
                frame = self.capture_frame()
                self.frame_count += 1
                
                # Detect or track cups
                if self.frame_count % 10 == 1:  # Re-detect every 10 frames
                    cups = self.detect_cups_color(frame)
                else:
                    cups = self.track_with_optical_flow(frame)
                
                self.cup_positions = cups
                self.update_tracking(cups)
                
                # Annotate
                annotated = self.draw_annotations(frame, cups)
                
                # Display
                cv2.imshow("Advanced Cup Tracker", annotated)
                
                # Input handling
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord('1') and len(cups) >= 1:
                    self.ball_cup_index = 0
                    print("Ball marked under Cup 1")
                elif key == ord('2') and len(cups) >= 2:
                    self.ball_cup_index = 1
                    print("Ball marked under Cup 2")
                elif key == ord('3') and len(cups) >= 3:
                    self.ball_cup_index = 2
                    print("Ball marked under Cup 3")
                elif key == ord('r'):
                    self.ball_cup_index = None
                    self.position_history = {0: deque(maxlen=50), 1: deque(maxlen=50), 2: deque(maxlen=50)}
                    print("Reset")
                
                # Store previous frame
                self.prev_frame = frame.copy()
                
        except KeyboardInterrupt:
            print("\nStopped")
        finally:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = AdvancedCupTracker()
    tracker.run()
