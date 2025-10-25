#!/usr/bin/env python3
"""
YOLO Object Tracker with ByteTrack/BoT-SORT
Advanced object tracking using YOLO detection and ByteTrack/BoT-SORT tracking algorithms.
Supports selected area detection from screen capture.
"""

import cv2
import numpy as np
import mss
from typing import List, Tuple, Optional, Dict
from collections import deque
from ultralytics import YOLO
import supervision as sv


class YOLOTracker:
    """Object tracking using YOLO detection and ByteTrack/BoT-SORT trackers."""
    
    def __init__(
        self, 
        screen_region: Optional[Dict] = None,
        model_name: str = "yolo11n.pt",
        tracker: str = "bytetrack",
        confidence: float = 0.25,
        iou: float = 0.45
    ):
        """
        Initialize the YOLO tracker.
        
        Args:
            screen_region: Dictionary with 'top', 'left', 'width', 'height' for screen capture.
                          If None, user will select region.
            model_name: YOLO model to use (yolo11n.pt, yolo11s.pt, yolo11m.pt, etc.)
            tracker: Tracker to use ('bytetrack' or 'botsort')
            confidence: Confidence threshold for detections (0.0-1.0)
            iou: IoU threshold for NMS (0.0-1.0)
        """
        self.screen_region = screen_region
        self.sct = None  # Lazy initialization
        
        # Initialize YOLO model
        print(f"Loading YOLO model: {model_name}")
        self.model = YOLO(model_name)
        
        # Tracking configuration
        self.tracker_type = tracker
        self.confidence = confidence
        self.iou = iou
        
        # State tracking
        self.track_history = {}  # Dictionary to store tracking history by ID
        self.ball_track_id = None  # Track ID of the object containing the ball
        self.frame_count = 0
        
        # Colors for visualization
        self.colors = sv.ColorPalette.DEFAULT
        
        # Supervision annotators
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.trace_annotator = sv.TraceAnnotator()
        
    def select_screen_region(self) -> Dict:
        """
        Allow user to select screen region to capture.
        Returns dictionary with screen region coordinates.
        """
        print("Select the screen region to track objects...")
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
    
    def track_objects(self, frame: np.ndarray) -> sv.Detections:
        """
        Track objects in the frame using YOLO and ByteTrack/BoT-SORT.
        
        Args:
            frame: Input frame
            
        Returns:
            Supervision Detections object with tracking information
        """
        # Run YOLO tracking
        results = self.model.track(
            frame,
            persist=True,
            tracker=f"{self.tracker_type}.yaml",
            conf=self.confidence,
            iou=self.iou,
            verbose=False
        )
        
        # Convert to supervision format
        if len(results) > 0 and results[0].boxes is not None:
            detections = sv.Detections.from_ultralytics(results[0])
            
            # Update tracking history
            if detections.tracker_id is not None:
                for i, track_id in enumerate(detections.tracker_id):
                    if track_id not in self.track_history:
                        self.track_history[track_id] = deque(maxlen=30)
                    
                    # Get center point
                    x1, y1, x2, y2 = detections.xyxy[i]
                    center = ((x1 + x2) / 2, (y1 + y2) / 2)
                    self.track_history[track_id].append(center)
            
            return detections
        
        return sv.Detections.empty()
    
    def annotate_frame(self, frame: np.ndarray, detections: sv.Detections) -> np.ndarray:
        """
        Annotate the frame with tracking information.
        
        Args:
            frame: Input frame
            detections: Detections with tracking information
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        if len(detections) > 0:
            # Create labels with tracking IDs and class names
            labels = []
            for i in range(len(detections)):
                track_id = detections.tracker_id[i] if detections.tracker_id is not None else None
                class_id = detections.class_id[i] if detections.class_id is not None else 0
                confidence = detections.confidence[i] if detections.confidence is not None else 0
                
                class_name = self.model.names[class_id] if class_id in self.model.names else f"class_{class_id}"
                
                if track_id is not None:
                    label = f"#{track_id} {class_name} {confidence:.2f}"
                    
                    # Highlight ball container
                    if track_id == self.ball_track_id:
                        label = f"⚽ BALL: {label}"
                else:
                    label = f"{class_name} {confidence:.2f}"
                
                labels.append(label)
            
            # Draw boxes and labels
            annotated = self.box_annotator.annotate(
                scene=annotated,
                detections=detections
            )
            annotated = self.label_annotator.annotate(
                scene=annotated,
                detections=detections,
                labels=labels
            )
            
            # Draw trajectories
            annotated = self.trace_annotator.annotate(
                scene=annotated,
                detections=detections
            )
            
            # Draw custom trajectory from history (for more control)
            if detections.tracker_id is not None:
                for i, track_id in enumerate(detections.tracker_id):
                    if track_id in self.track_history and len(self.track_history[track_id]) > 1:
                        points = list(self.track_history[track_id])
                        
                        # Different color if it's the ball container
                        color = (0, 255, 255) if track_id == self.ball_track_id else (255, 0, 255)
                        
                        for j in range(1, len(points)):
                            pt1 = (int(points[j-1][0]), int(points[j-1][1]))
                            pt2 = (int(points[j][0]), int(points[j][1]))
                            cv2.line(annotated, pt1, pt2, color, 2)
        
        # Display info
        info_text = f"Tracker: {self.tracker_type.upper()} | Model: {self.model.model_name} | Objects: {len(detections)}"
        cv2.putText(annotated, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display ball tracking status
        if self.ball_track_id is not None:
            ball_text = f"Tracking Ball -> ID #{self.ball_track_id}"
            cv2.putText(annotated, ball_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Display controls
        controls = "Controls: [S]elect object | [R]eset | [Q]uit"
        cv2.putText(annotated, controls, (10, frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated
    
    def mark_ball_position(self, detections: sv.Detections, point: Tuple[int, int]):
        """
        Mark which object contains the ball based on click position.
        
        Args:
            detections: Current detections
            point: (x, y) point clicked by user
        """
        if len(detections) == 0 or detections.tracker_id is None:
            print("No tracked objects found")
            return
        
        # Find which detection contains the point
        for i, (x1, y1, x2, y2) in enumerate(detections.xyxy):
            if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
                track_id = detections.tracker_id[i]
                self.ball_track_id = track_id
                print(f"Ball marked in object with Track ID #{track_id}")
                return
        
        print("No object found at clicked position")
    
    def run(self):
        """Main loop to run the YOLO tracking system."""
        print("=" * 60)
        print("YOLO Object Tracker with ByteTrack/BoT-SORT")
        print("=" * 60)
        print(f"Tracker: {self.tracker_type.upper()}")
        print(f"Model: {self.model.model_name}")
        print(f"Confidence: {self.confidence}")
        print(f"IoU: {self.iou}")
        print()
        print("Controls:")
        print("  Click on object: Mark as ball container")
        print("  R: Reset ball tracking")
        print("  Q: Quit")
        print()
        
        # Mouse callback state
        click_point = None
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal click_point
            if event == cv2.EVENT_LBUTTONDOWN:
                click_point = (x, y)
        
        try:
            window_name = "YOLO Object Tracker"
            cv2.namedWindow(window_name)
            cv2.setMouseCallback(window_name, mouse_callback)
            
            while True:
                # Capture frame
                frame = self.capture_frame()
                self.frame_count += 1
                
                # Track objects
                detections = self.track_objects(frame)
                
                # Handle click to mark ball
                if click_point is not None:
                    self.mark_ball_position(detections, click_point)
                    click_point = None
                
                # Annotate frame
                annotated = self.annotate_frame(frame, detections)
                
                # Display
                cv2.imshow(window_name, annotated)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('r'):
                    self.ball_track_id = None
                    print("Ball tracking reset")
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cv2.destroyAllWindows()
            if self.sct is not None:
                self.sct.close()


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("  YOLO Object Tracking System")
    print("  with ByteTrack/BoT-SORT Trackers")
    print("=" * 60)
    print()
    
    import argparse
    parser = argparse.ArgumentParser(description="YOLO Object Tracker")
    parser.add_argument("--model", default="yolo11n.pt", 
                       help="YOLO model (yolo11n.pt, yolo11s.pt, yolo11m.pt, etc.)")
    parser.add_argument("--tracker", default="bytetrack", choices=["bytetrack", "botsort"],
                       help="Tracker to use (bytetrack or botsort)")
    parser.add_argument("--conf", type=float, default=0.25,
                       help="Confidence threshold (0.0-1.0)")
    parser.add_argument("--iou", type=float, default=0.45,
                       help="IoU threshold for NMS (0.0-1.0)")
    
    args = parser.parse_args()
    
    # Create tracker instance
    tracker = YOLOTracker(
        model_name=args.model,
        tracker=args.tracker,
        confidence=args.conf,
        iou=args.iou
    )
    
    # Run the tracker
    tracker.run()


if __name__ == "__main__":
    main()
