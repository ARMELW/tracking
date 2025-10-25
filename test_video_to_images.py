#!/usr/bin/env python3
"""
Test script for video_to_images module.
"""

import cv2
import numpy as np
import os
import tempfile
import shutil
from video_to_images import VideoToImages


def create_test_video(filename, num_frames=30, fps=10, width=320, height=240):
    """Create a simple test video with frame numbers displayed."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    for i in range(num_frames):
        # Create frame with gradient background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = (i * 8 % 255, (i * 5) % 255, (i * 3) % 255)
        
        # Add frame number
        text = f"Frame {i}"
        cv2.putText(frame, text, (50, height // 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"Created test video: {filename} with {num_frames} frames")


def test_basic_extraction():
    """Test basic frame extraction."""
    print("\n" + "=" * 60)
    print("Test 1: Basic Frame Extraction")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=30)
        
        # Extract frames
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir, format="png")
        extracted = converter.extract_frames()
        
        # Verify
        assert extracted == 30, f"Expected 30 frames, got {extracted}"
        assert os.path.exists(output_dir), "Output directory not created"
        
        # Check files
        files = os.listdir(output_dir)
        assert len(files) == 30, f"Expected 30 files, got {len(files)}"
        
        print("✓ Basic extraction test passed")
        return True


def test_step_extraction():
    """Test extraction with step parameter."""
    print("\n" + "=" * 60)
    print("Test 2: Step Extraction (every 5th frame)")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=50)
        
        # Extract every 5th frame
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir)
        extracted = converter.extract_frames(step=5)
        
        # Verify
        expected = 10  # 50 frames / 5 = 10 frames
        assert extracted == expected, f"Expected {expected} frames, got {extracted}"
        
        print(f"✓ Step extraction test passed (extracted {extracted} frames)")
        return True


def test_range_extraction():
    """Test extraction with start and end frame."""
    print("\n" + "=" * 60)
    print("Test 3: Range Extraction (frames 10-20)")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=30)
        
        # Extract frames 10-20
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir)
        extracted = converter.extract_frames(start_frame=10, end_frame=20)
        
        # Verify
        expected = 10  # frames 10-19 (10 frames total)
        assert extracted == expected, f"Expected {expected} frames, got {extracted}"
        
        print(f"✓ Range extraction test passed (extracted {extracted} frames)")
        return True


def test_max_frames():
    """Test extraction with max frames limit."""
    print("\n" + "=" * 60)
    print("Test 4: Max Frames Limit (max 15 frames)")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=50)
        
        # Extract max 15 frames
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir)
        extracted = converter.extract_frames(max_frames=15)
        
        # Verify
        assert extracted == 15, f"Expected 15 frames, got {extracted}"
        
        print(f"✓ Max frames test passed (extracted {extracted} frames)")
        return True


def test_specific_frames():
    """Test extraction of specific frames."""
    print("\n" + "=" * 60)
    print("Test 5: Specific Frames Extraction")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=30)
        
        # Extract specific frames
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir)
        frame_numbers = [0, 5, 10, 15, 20, 25]
        extracted = converter.extract_specific_frames(frame_numbers)
        
        # Verify
        assert extracted == len(frame_numbers), f"Expected {len(frame_numbers)} frames, got {extracted}"
        
        print(f"✓ Specific frames test passed (extracted {extracted} frames)")
        return True


def test_jpg_format():
    """Test JPG format output."""
    print("\n" + "=" * 60)
    print("Test 6: JPG Format Output")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test video
        video_path = os.path.join(tmpdir, "test_video.mp4")
        create_test_video(video_path, num_frames=10)
        
        # Extract as JPG
        output_dir = os.path.join(tmpdir, "frames")
        converter = VideoToImages(video_path, output_dir=output_dir, format="jpg")
        extracted = converter.extract_frames()
        
        # Verify
        assert extracted == 10, f"Expected 10 frames, got {extracted}"
        
        # Check file format
        files = [f for f in os.listdir(output_dir) if f.endswith('.jpg')]
        assert len(files) == 10, f"Expected 10 JPG files, got {len(files)}"
        
        print("✓ JPG format test passed")
        return True


def test_file_not_found():
    """Test handling of non-existent video file."""
    print("\n" + "=" * 60)
    print("Test 7: File Not Found Error Handling")
    print("=" * 60)
    
    try:
        converter = VideoToImages("nonexistent_video.mp4")
        print("✗ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        print(f"✓ Correctly raised FileNotFoundError: {e}")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Video to Images Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Extraction", test_basic_extraction),
        ("Step Extraction", test_step_extraction),
        ("Range Extraction", test_range_extraction),
        ("Max Frames", test_max_frames),
        ("Specific Frames", test_specific_frames),
        ("JPG Format", test_jpg_format),
        ("File Not Found", test_file_not_found),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
