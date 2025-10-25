#!/usr/bin/env python3
"""
Video to Images Converter
Extracts frames from video files and saves them as individual images.
"""

import cv2
import os
import argparse
import sys
from pathlib import Path
from typing import Optional


class VideoToImages:
    """Convert video files to individual image frames."""
    
    def __init__(self, video_path: str, output_dir: str = None, 
                 format: str = "png", prefix: str = "frame"):
        """
        Initialize the video to images converter.
        
        Args:
            video_path: Path to the input video file
            output_dir: Directory to save extracted frames (default: video_name_frames/)
            format: Output image format ('png' or 'jpg', default: 'png')
            prefix: Prefix for output filenames (default: 'frame')
        """
        self.video_path = video_path
        self.format = format.lower()
        self.prefix = prefix
        
        # Validate video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Set output directory
        if output_dir is None:
            video_name = Path(video_path).stem
            self.output_dir = f"{video_name}_frames"
        else:
            self.output_dir = output_dir
        
        # Validate format
        if self.format not in ['png', 'jpg', 'jpeg']:
            raise ValueError(f"Unsupported format: {format}. Use 'png' or 'jpg'")
        
        # Normalize jpeg format
        if self.format == 'jpeg':
            self.format = 'jpg'
    
    def extract_frames(self, start_frame: int = 0, end_frame: Optional[int] = None,
                      step: int = 1, max_frames: Optional[int] = None) -> int:
        """
        Extract frames from the video and save as images.
        
        Args:
            start_frame: Frame number to start extraction (default: 0)
            end_frame: Frame number to end extraction (default: None, extract all)
            step: Extract every Nth frame (default: 1, extract all frames)
            max_frames: Maximum number of frames to extract (default: None, no limit)
        
        Returns:
            Number of frames extracted
        """
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.video_path}")
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Video: {self.video_path}")
        print(f"  Total frames: {total_frames}")
        print(f"  FPS: {fps:.2f}")
        print(f"  Resolution: {width}x{height}")
        print(f"  Duration: {total_frames/fps:.2f} seconds")
        print()
        
        # Set end frame
        if end_frame is None:
            end_frame = total_frames
        else:
            end_frame = min(end_frame, total_frames)
        
        # Extract frames
        frame_count = 0
        extracted_count = 0
        
        print(f"Extracting frames to: {self.output_dir}/")
        print(f"  Start frame: {start_frame}")
        print(f"  End frame: {end_frame}")
        print(f"  Step: {step}")
        print(f"  Format: {self.format}")
        print()
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Check if we should extract this frame
                if frame_count >= start_frame and frame_count < end_frame:
                    if (frame_count - start_frame) % step == 0:
                        # Check max frames limit
                        if max_frames is not None and extracted_count >= max_frames:
                            print(f"\nReached maximum frame limit ({max_frames})")
                            break
                        
                        # Generate filename with zero-padding
                        filename = f"{self.prefix}_{frame_count:06d}.{self.format}"
                        output_path = os.path.join(self.output_dir, filename)
                        
                        # Save frame
                        cv2.imwrite(output_path, frame)
                        extracted_count += 1
                        
                        # Progress indicator
                        if extracted_count % 10 == 0:
                            print(f"Extracted {extracted_count} frames...", end='\r')
                
                frame_count += 1
                
                # Check if we've reached the end frame
                if frame_count >= end_frame:
                    break
            
            print(f"\nExtraction complete!")
            print(f"Total frames extracted: {extracted_count}")
            print(f"Saved to: {os.path.abspath(self.output_dir)}/")
            
        finally:
            cap.release()
        
        return extracted_count
    
    def extract_specific_frames(self, frame_numbers: list) -> int:
        """
        Extract specific frames by frame number.
        
        Args:
            frame_numbers: List of frame numbers to extract
        
        Returns:
            Number of frames extracted
        """
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Extracting {len(frame_numbers)} specific frames...")
        
        extracted_count = 0
        
        try:
            for frame_num in sorted(frame_numbers):
                if frame_num >= total_frames:
                    print(f"Warning: Frame {frame_num} exceeds video length")
                    continue
                
                # Seek to frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                
                if ret:
                    filename = f"{self.prefix}_{frame_num:06d}.{self.format}"
                    output_path = os.path.join(self.output_dir, filename)
                    cv2.imwrite(output_path, frame)
                    extracted_count += 1
                    
                    if extracted_count % 10 == 0:
                        print(f"Extracted {extracted_count} frames...", end='\r')
            
            print(f"\nExtraction complete!")
            print(f"Total frames extracted: {extracted_count}")
            print(f"Saved to: {os.path.abspath(self.output_dir)}/")
            
        finally:
            cap.release()
        
        return extracted_count


def main():
    """Command-line interface for video to images converter."""
    parser = argparse.ArgumentParser(
        description="Extract frames from video files as individual images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all frames from a video
  python video_to_images.py input.mp4
  
  # Extract frames with custom output directory
  python video_to_images.py input.mp4 -o output_frames/
  
  # Extract every 10th frame as JPG
  python video_to_images.py input.mp4 --step 10 --format jpg
  
  # Extract frames 100 to 200
  python video_to_images.py input.mp4 --start 100 --end 200
  
  # Extract first 50 frames
  python video_to_images.py input.mp4 --max 50
  
  # Extract specific frames
  python video_to_images.py input.mp4 --frames 0 10 20 30 40
        """
    )
    
    parser.add_argument("video", help="Path to input video file")
    parser.add_argument("-o", "--output", help="Output directory for frames")
    parser.add_argument("-f", "--format", choices=["png", "jpg", "jpeg"],
                       default="png", help="Output image format (default: png)")
    parser.add_argument("-p", "--prefix", default="frame",
                       help="Prefix for output filenames (default: frame)")
    parser.add_argument("--start", type=int, default=0,
                       help="Start frame number (default: 0)")
    parser.add_argument("--end", type=int, default=None,
                       help="End frame number (default: extract all)")
    parser.add_argument("--step", type=int, default=1,
                       help="Extract every Nth frame (default: 1)")
    parser.add_argument("--max", type=int, default=None,
                       help="Maximum number of frames to extract (default: no limit)")
    parser.add_argument("--frames", type=int, nargs="+",
                       help="Extract specific frame numbers")
    
    args = parser.parse_args()
    
    try:
        # Create converter
        converter = VideoToImages(
            video_path=args.video,
            output_dir=args.output,
            format=args.format,
            prefix=args.prefix
        )
        
        # Extract frames
        if args.frames:
            converter.extract_specific_frames(args.frames)
        else:
            converter.extract_frames(
                start_frame=args.start,
                end_frame=args.end,
                step=args.step,
                max_frames=args.max
            )
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
