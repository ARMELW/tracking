#!/usr/bin/env python3
"""
Demo script for video_to_images module.
Creates a sample video and extracts frames from it.
"""

import cv2
import numpy as np
import os
import tempfile
from video_to_images import VideoToImages


def create_animated_demo_video(filename, duration_sec=3, fps=30):
    """
    Create a demo video with animated content.
    
    Args:
        filename: Output video filename
        duration_sec: Video duration in seconds
        fps: Frames per second
    """
    width, height = 640, 480
    num_frames = duration_sec * fps
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    print(f"Creating demo video...")
    print(f"  Duration: {duration_sec} seconds")
    print(f"  FPS: {fps}")
    print(f"  Total frames: {num_frames}")
    print()
    
    for i in range(num_frames):
        # Create colorful animated frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animated gradient background
        for y in range(height):
            color_val = int(127 + 127 * np.sin(2 * np.pi * (i / num_frames + y / height)))
            frame[y, :] = (color_val, 255 - color_val, (color_val + 128) % 255)
        
        # Draw moving circle
        circle_x = int(width * (0.5 + 0.3 * np.cos(2 * np.pi * i / num_frames)))
        circle_y = int(height * (0.5 + 0.3 * np.sin(2 * np.pi * i / num_frames)))
        cv2.circle(frame, (circle_x, circle_y), 40, (255, 255, 255), -1)
        cv2.circle(frame, (circle_x, circle_y), 40, (0, 0, 0), 3)
        
        # Add frame number and timestamp
        text = f"Frame: {i}/{num_frames}"
        cv2.putText(frame, text, (20, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        time_text = f"Time: {i/fps:.2f}s"
        cv2.putText(frame, time_text, (20, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        out.write(frame)
        
        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1}/{num_frames} frames...", end='\r')
    
    out.release()
    print(f"\n✓ Demo video created: {filename}")
    print()


def run_demo():
    """Run the video to images demo."""
    print("=" * 70)
    print("  Video to Images Converter - Demo")
    print("=" * 70)
    print()
    
    # Create temporary directory for demo
    demo_dir = "/tmp/video_to_images_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Create demo video
    video_path = os.path.join(demo_dir, "demo_video.mp4")
    create_animated_demo_video(video_path, duration_sec=3, fps=30)
    
    # Demo 1: Extract all frames
    print("=" * 70)
    print("Demo 1: Extract All Frames")
    print("=" * 70)
    print()
    
    output_dir_1 = os.path.join(demo_dir, "all_frames")
    converter = VideoToImages(video_path, output_dir=output_dir_1, format="png")
    converter.extract_frames()
    print()
    
    # Demo 2: Extract every 5th frame
    print("=" * 70)
    print("Demo 2: Extract Every 5th Frame")
    print("=" * 70)
    print()
    
    output_dir_2 = os.path.join(demo_dir, "every_5th_frame")
    converter = VideoToImages(video_path, output_dir=output_dir_2, format="jpg")
    converter.extract_frames(step=5)
    print()
    
    # Demo 3: Extract first 10 frames
    print("=" * 70)
    print("Demo 3: Extract First 10 Frames")
    print("=" * 70)
    print()
    
    output_dir_3 = os.path.join(demo_dir, "first_10_frames")
    converter = VideoToImages(video_path, output_dir=output_dir_3)
    converter.extract_frames(max_frames=10)
    print()
    
    # Demo 4: Extract specific frames
    print("=" * 70)
    print("Demo 4: Extract Specific Frames (0, 15, 30, 45, 60, 75)")
    print("=" * 70)
    print()
    
    output_dir_4 = os.path.join(demo_dir, "specific_frames")
    converter = VideoToImages(video_path, output_dir=output_dir_4)
    converter.extract_specific_frames([0, 15, 30, 45, 60, 75])
    print()
    
    # Summary
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print(f"Demo files saved to: {demo_dir}/")
    print()
    print("Directories created:")
    print(f"  1. {output_dir_1}/ - All frames (90 PNG images)")
    print(f"  2. {output_dir_2}/ - Every 5th frame (18 JPG images)")
    print(f"  3. {output_dir_3}/ - First 10 frames (10 PNG images)")
    print(f"  4. {output_dir_4}/ - Specific frames (6 PNG images)")
    print()
    print("You can view these images with any image viewer.")
    print()
    
    # Display one extracted frame as a demonstration
    try:
        sample_frame_path = os.path.join(output_dir_1, "frame_000000.png")
        if os.path.exists(sample_frame_path):
            print("Sample extracted frame preview:")
            frame = cv2.imread(sample_frame_path)
            print(f"  File: {sample_frame_path}")
            print(f"  Size: {frame.shape[1]}x{frame.shape[0]}")
            print(f"  Format: PNG")
    except Exception as e:
        print(f"Note: Could not load sample frame for preview: {e}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
