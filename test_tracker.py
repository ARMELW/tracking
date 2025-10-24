#!/usr/bin/env python3
"""
Simple test script to verify the tracking modules can be imported
and basic functionality works.
"""

import sys


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import mss
        print(f"✓ MSS")
    except ImportError as e:
        print(f"✗ MSS import failed: {e}")
        return False
    
    return True


def test_tracker_imports():
    """Test that tracker modules can be imported."""
    print("\nTesting tracker imports...")
    
    try:
        from cup_tracker import CupTracker
        print("✓ CupTracker imported successfully")
    except ImportError as e:
        print(f"✗ CupTracker import failed: {e}")
        return False
    
    try:
        from advanced_tracker import AdvancedCupTracker
        print("✓ AdvancedCupTracker imported successfully")
    except ImportError as e:
        print(f"✗ AdvancedCupTracker import failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality without GUI."""
    print("\nTesting basic functionality...")
    
    try:
        import numpy as np
        from cup_tracker import CupTracker
        
        # Create a tracker with a dummy region (no display needed yet)
        screen_region = {"top": 0, "left": 0, "width": 640, "height": 480}
        tracker = CupTracker(screen_region=screen_region)
        print(f"✓ Tracker created successfully")
        
        # Test cup detection on a dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cups = tracker.detect_cups(dummy_frame)
        print(f"✓ Cup detection works (found {len(cups)} cups in test frame)")
        
        # Test annotation
        annotated = tracker.annotate_frame(dummy_frame)
        print(f"✓ Frame annotation works")
        
        # Test tracking methods
        tracker.track_cup_movements(cups)
        print(f"✓ Cup tracking works")
        
        # Test prediction
        tracker.last_known_ball_position = 0
        prediction = tracker.predict_ball_position()
        print(f"✓ Ball prediction works (predicted: {prediction})")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Cup Tracker Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Tracker Imports", test_tracker_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))
    
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
