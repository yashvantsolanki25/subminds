"""Test if all imports work"""
import sys

print("Testing imports...")
print(f"Python: {sys.version}")

try:
    import cv2
    print("✓ OpenCV (cv2) imported successfully")
    print(f"  Version: {cv2.__version__}")
except ImportError as e:
    print(f"✗ OpenCV import failed: {e}")

try:
    import numpy
    print("✓ NumPy imported successfully")
    print(f"  Version: {numpy.__version__}")
except ImportError as e:
    print(f"✗ NumPy import failed: {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except ImportError as e:
    print(f"✗ python-dotenv import failed: {e}")

try:
    import tkinter
    print("✓ tkinter imported successfully")
except ImportError as e:
    print(f"✗ tkinter import failed: {e}")

print("\nNow testing SubMinds modules...")

try:
    from src.facial_analysis.capture import FacialCapture
    print("✓ FacialCapture imported successfully")
except ImportError as e:
    print(f"✗ FacialCapture import failed: {e}")

try:
    from src.facial_analysis.emotion_tracker import EmotionTracker
    print("✓ EmotionTracker imported successfully")
except ImportError as e:
    print(f"✗ EmotionTracker import failed: {e}")

try:
    from src.ai_engine.granite_client import GraniteAIClient
    print("✓ GraniteAIClient imported successfully")
except ImportError as e:
    print(f"✗ GraniteAIClient import failed: {e}")

print("\nAll tests complete!")

# Made with Bob
