#!/usr/bin/env python3
"""
Test script for YOLO tracker functionality.
"""

import sys
import numpy as np


def test_yolo_imports():
    """Test that YOLO-related modules can be imported."""
    print("Testing YOLO imports...")
    
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO imported successfully")
    except ImportError as e:
        print(f"✗ Ultralytics import failed: {e}")
        return False
    
    try:
        import supervision as sv
        print("✓ Supervision imported successfully")
    except ImportError as e:
        print(f"✗ Supervision import failed: {e}")
        return False
    
    return True


def test_yolo_tracker_import():
    """Test that YOLOTracker can be imported."""
    print("\nTesting YOLOTracker import...")
    
    try:
        from yolo_tracker import YOLOTracker
        print("✓ YOLOTracker imported successfully")
        return True
    except ImportError as e:
        print(f"✗ YOLOTracker import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_yolo_tracker_initialization():
    """Test that YOLOTracker can be initialized."""
    print("\nTesting YOLOTracker initialization...")
    
    try:
        from yolo_tracker import YOLOTracker
        import supervision as sv
        
        # Create a tracker with a dummy region (no display needed yet)
        screen_region = {"top": 0, "left": 0, "width": 640, "height": 480}
        tracker = YOLOTracker(
            screen_region=screen_region,
            model_name="yolo11n.pt",
            tracker="bytetrack",
            confidence=0.25,
            iou=0.45
        )
        print("✓ YOLOTracker initialized successfully")
        
        # Test tracking on a dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = tracker.track_objects(dummy_frame)
        print(f"✓ Object tracking works (found {len(detections)} objects in test frame)")
        
        # Test annotation
        annotated = tracker.annotate_frame(dummy_frame, detections)
        print("✓ Frame annotation works")
        
        return True
    except Exception as e:
        print(f"✗ YOLOTracker initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_supervision_detections():
    """Test Supervision detections functionality."""
    print("\nTesting Supervision detections...")
    
    try:
        import supervision as sv
        
        # Create empty detections
        detections = sv.Detections.empty()
        print(f"✓ Empty detections created: {len(detections)} objects")
        
        # Create detections with data
        xyxy = np.array([[10, 10, 100, 100], [200, 200, 300, 300]])
        confidence = np.array([0.9, 0.8])
        class_id = np.array([0, 1])
        tracker_id = np.array([1, 2])
        
        detections = sv.Detections(
            xyxy=xyxy,
            confidence=confidence,
            class_id=class_id,
            tracker_id=tracker_id
        )
        print(f"✓ Detections created with {len(detections)} objects")
        
        # Test annotators
        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        trace_annotator = sv.TraceAnnotator()
        print("✓ Annotators created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Supervision detections test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("YOLO Tracker Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("YOLO Imports", test_yolo_imports()))
    results.append(("YOLOTracker Import", test_yolo_tracker_import()))
    results.append(("Supervision Detections", test_supervision_detections()))
    results.append(("YOLOTracker Initialization", test_yolo_tracker_initialization()))
    
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
    sys.exit(main())
