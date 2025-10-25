#!/usr/bin/env python3
"""
Tests for Screen Recorder
"""

import unittest
import os
import sys
import tempfile
import shutil
import numpy as np
import cv2
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from screen_recorder import ScreenRecorder


class TestScreenRecorder(unittest.TestCase):
    """Test cases for ScreenRecorder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_output = os.path.join(self.test_dir, "test_recording.mp4")
        
        # Define a test screen region (small for testing)
        self.test_region = {
            "top": 0,
            "left": 0,
            "width": 320,
            "height": 240
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test ScreenRecorder initialization."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            fps=30,
            screen_region=self.test_region
        )
        
        self.assertEqual(recorder.output_path, self.test_output)
        self.assertEqual(recorder.fps, 30)
        self.assertFalse(recorder.is_recording)
        self.assertEqual(recorder.frames_recorded, 0)
    
    def test_initialization_default_output(self):
        """Test ScreenRecorder initialization with default output path."""
        recorder = ScreenRecorder()
        
        self.assertTrue(recorder.output_path.startswith("screen_recording_"))
        self.assertTrue(recorder.output_path.endswith(".mp4"))
    
    def test_initialization_adds_mp4_extension(self):
        """Test that .mp4 extension is added if missing."""
        recorder = ScreenRecorder(output_path="test_video")
        
        self.assertEqual(recorder.output_path, "test_video.mp4")
    
    def test_start_recording(self):
        """Test starting recording."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        
        self.assertTrue(recorder.is_recording)
        self.assertIsNotNone(recorder.video_writer)
        self.assertEqual(recorder.frames_recorded, 0)
        
        # Cleanup
        recorder.stop_recording()
    
    def test_stop_recording(self):
        """Test stopping recording."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        recorder.stop_recording()
        
        self.assertFalse(recorder.is_recording)
        self.assertIsNone(recorder.video_writer)
    
    def test_record_frame(self):
        """Test recording a frame."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        # Create test frame
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        
        recorder.start_recording()
        initial_count = recorder.frames_recorded
        
        recorder.record_frame(frame)
        
        self.assertEqual(recorder.frames_recorded, initial_count + 1)
        
        # Cleanup
        recorder.stop_recording()
    
    def test_record_multiple_frames(self):
        """Test recording multiple frames."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        
        # Record 10 frames
        for i in range(10):
            frame = np.zeros((240, 320, 3), dtype=np.uint8)
            frame[:] = (i * 10, i * 10, i * 10)  # Vary intensity
            recorder.record_frame(frame)
        
        self.assertEqual(recorder.frames_recorded, 10)
        
        recorder.stop_recording()
        
        # Check that file was created
        self.assertTrue(os.path.exists(self.test_output))
        
        # Check that file has content
        self.assertGreater(os.path.getsize(self.test_output), 0)
    
    def test_annotate_frame_not_recording(self):
        """Test frame annotation when not recording."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        annotated = recorder.annotate_frame(frame)
        
        self.assertEqual(annotated.shape, frame.shape)
        self.assertFalse(np.array_equal(annotated, frame))  # Should be different (annotated)
    
    def test_annotate_frame_recording(self):
        """Test frame annotation when recording."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        annotated = recorder.annotate_frame(frame)
        
        self.assertEqual(annotated.shape, frame.shape)
        self.assertFalse(np.array_equal(annotated, frame))  # Should be different (annotated)
        
        recorder.stop_recording()
    
    def test_video_file_properties(self):
        """Test that recorded video has correct properties."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            fps=30,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        
        # Record 30 frames (1 second at 30 FPS)
        for i in range(30):
            frame = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
            recorder.record_frame(frame)
        
        recorder.stop_recording()
        
        # Open video and check properties
        cap = cv2.VideoCapture(self.test_output)
        
        self.assertTrue(cap.isOpened())
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        self.assertEqual(width, 320)
        self.assertEqual(height, 240)
        self.assertEqual(fps, 30.0)
        self.assertEqual(frame_count, 30)
        
        cap.release()
    
    def test_stop_when_not_recording(self):
        """Test stopping when not recording (should not raise error)."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        # Should not raise an exception
        recorder.stop_recording()
        
        self.assertFalse(recorder.is_recording)
    
    def test_start_when_already_recording(self):
        """Test starting when already recording (should not start again)."""
        recorder = ScreenRecorder(
            output_path=self.test_output,
            screen_region=self.test_region
        )
        
        recorder.start_recording()
        first_writer = recorder.video_writer
        
        recorder.start_recording()  # Try to start again
        
        # Should still be the same writer
        self.assertEqual(recorder.video_writer, first_writer)
        
        recorder.stop_recording()


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestScreenRecorder)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
