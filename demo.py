#!/usr/bin/env python3
"""
Demo script showing cup tracking on a synthetic video.
This can be used for testing without needing actual screen capture.
"""

import cv2
import numpy as np
from cup_tracker import CupTracker
import time


def create_synthetic_cup_frame(width=800, height=600, cup_positions=None):
    """
    Create a synthetic frame with cup-like shapes.
    
    Args:
        width: Frame width
        height: Frame height
        cup_positions: List of (x, y) positions for cups
    
    Returns:
        Synthetic frame with cups
    """
    frame = np.ones((height, width, 3), dtype=np.uint8) * 240  # Light background
    
    if cup_positions is None:
        cup_positions = [(150, 300), (400, 300), (650, 300)]
    
    # Draw cup-like shapes
    for x, y in cup_positions:
        # Draw trapezoid shape (cup)
        pts = np.array([
            [x - 40, y],
            [x + 40, y],
            [x + 30, y - 80],
            [x - 30, y - 80]
        ], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(frame, [pts], (100, 100, 200))
        cv2.polylines(frame, [pts], True, (50, 50, 150), 3)
    
    return frame


def simulate_cup_movement(start_pos, end_pos, frames=30):
    """
    Generate smooth movement between two positions.
    
    Args:
        start_pos: Starting (x, y) position
        end_pos: Ending (x, y) position
        frames: Number of frames for the transition
    
    Returns:
        List of (x, y) positions
    """
    positions = []
    for i in range(frames):
        t = i / (frames - 1) if frames > 1 else 0
        x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * t)
        y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * t)
        positions.append((x, y))
    return positions


def run_demo(save_video=False, output_file="/tmp/cup_tracking_demo.avi"):
    """
    Run a demonstration of the cup tracking system.
    
    Args:
        save_video: If True, save the output video
        output_file: Path to save output video
    """
    print("=" * 60)
    print("Cup Tracking Demo - Synthetic Video")
    print("=" * 60)
    print()
    
    # Setup video writer if saving
    video_writer = None
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(output_file, fourcc, 20.0, (800, 600))
    
    # Define initial cup positions
    initial_positions = [(150, 400), (400, 400), (650, 400)]
    
    # Simulate a shuffle: swap cups 0 and 2
    shuffle_sequence = [
        # Phase 1: Move cup 0 right and cup 2 left (start of swap)
        {
            0: simulate_cup_movement((150, 400), (400, 300), 20),
            1: [(400, 400)] * 20,
            2: simulate_cup_movement((650, 400), (400, 300), 20)
        },
        # Phase 2: Cross over
        {
            0: simulate_cup_movement((400, 300), (650, 400), 20),
            1: [(400, 400)] * 20,
            2: simulate_cup_movement((400, 300), (150, 400), 20)
        },
        # Phase 3: Settle
        {
            0: [(650, 400)] * 10,
            1: [(400, 400)] * 10,
            2: [(150, 400)] * 10
        }
    ]
    
    # Create tracker (will work without display for detection only)
    tracker = CupTracker(screen_region={"top": 0, "left": 0, "width": 800, "height": 600})
    
    # Mark ball initially under cup 1 (index 0)
    tracker.last_known_ball_position = 0
    print("Ball initially placed under Cup 1 (leftmost)")
    print("Starting shuffle sequence...")
    print()
    
    frame_count = 0
    
    # Generate and process frames
    for phase_idx, phase in enumerate(shuffle_sequence):
        print(f"Phase {phase_idx + 1}...")
        
        num_frames = len(phase[0])
        for frame_idx in range(num_frames):
            # Get current positions
            current_positions = [
                phase[0][frame_idx],
                phase[1][frame_idx],
                phase[2][frame_idx]
            ]
            
            # Create synthetic frame
            frame = create_synthetic_cup_frame(cup_positions=current_positions)
            
            # Process with tracker
            annotated = tracker.annotate_frame(frame)
            
            # Add frame number
            cv2.putText(annotated, f"Frame: {frame_count}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            
            # Display prediction
            prediction = tracker.predict_ball_position()
            if prediction is not None:
                # After shuffle, cup 0 (originally left) is now rightmost (position 2)
                # Cup 2 (originally right) is now leftmost (position 0)
                text = f"Predicted: Cup at position {prediction + 1}"
                cv2.putText(annotated, text, (10, 560),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Save or display
            if save_video and video_writer:
                video_writer.write(annotated)
            
            # Show frame (only works with display)
            try:
                cv2.imshow("Cup Tracking Demo", annotated)
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    print("Demo interrupted by user")
                    break
            except cv2.error:
                # No display available, just continue
                pass
            
            frame_count += 1
        
        # Small pause between phases (in display mode)
        time.sleep(0.1)
    
    # Cleanup
    if video_writer:
        video_writer.release()
        print(f"\nVideo saved to: {output_file}")
    
    cv2.destroyAllWindows()
    
    print()
    print("=" * 60)
    print("Demo completed!")
    print(f"Processed {frame_count} frames")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # Check if user wants to save video
    save_video = "--save" in sys.argv
    
    if save_video:
        print("Video will be saved to /tmp/cup_tracking_demo.avi")
        print()
    
    run_demo(save_video=save_video)
