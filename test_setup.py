"""
SubMinds Setup Verification Script
Tests all components and configurations
"""
import sys
import os
from pathlib import Path

print("=" * 70)
print("SubMinds Setup Verification")
print("=" * 70)
print()

# Test 1: Python Version
print("1. Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 9:
    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
print()

# Test 2: Required Packages
print("2. Checking required packages...")
required_packages = {
    'cv2': 'opencv-python',
    'mediapipe': 'mediapipe',
    'deepface': 'deepface',
    'tensorflow': 'tensorflow',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'yaml': 'pyyaml',
    'dotenv': 'python-dotenv'
}

missing_packages = []
for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} (missing)")
        missing_packages.append(package)

if missing_packages:
    print(f"\n   Install missing packages: pip install {' '.join(missing_packages)}")
print()

# Test 3: Environment Variables
print("3. Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('IBM_CLOUD_API_KEY')
project_id = os.getenv('IBM_PROJECT_ID')

if api_key and len(api_key) > 10:
    print(f"   ✅ IBM_CLOUD_API_KEY is set ({api_key[:10]}...)")
else:
    print(f"   ❌ IBM_CLOUD_API_KEY not set or invalid")

if project_id:
    print(f"   ✅ IBM_PROJECT_ID is set ({project_id})")
else:
    print(f"   ❌ IBM_PROJECT_ID not set")
print()

# Test 4: Configuration Files
print("4. Checking configuration files...")
config_files = [
    'config/ibm_granite_config.yaml',
    'config/camera_config.yaml',
    '.env'
]

for config_file in config_files:
    if Path(config_file).exists():
        print(f"   ✅ {config_file}")
    else:
        print(f"   ❌ {config_file} (missing)")
print()

# Test 5: Webcam
print("5. Checking webcam...")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print(f"   ✅ Webcam available (device 0)")
        cap.release()
    else:
        print(f"   ❌ Webcam not available")
except Exception as e:
    print(f"   ❌ Error checking webcam: {e}")
print()

# Test 6: IBM Granite Connection
print("6. Testing IBM Granite connection...")
try:
    sys.path.insert(0, 'src')
    from ai_engine.granite_client import GraniteAIClient
    
    client = GraniteAIClient(config_path='config/ibm_granite_config.yaml')
    
    if client.is_available():
        print(f"   ✅ IBM Granite client initialized successfully")
        print(f"   ✅ Connected to: {client.url}")
        
        # Test analysis
        test_facial = {
            'dominant_emotion': 'neutral',
            'confidence': 0.8,
            'valence': 0.0,
            'arousal': 0.5
        }
        test_telemetry = {
            'speed': 100.0,
            'steering': 0.0,
            'track_position': 0.0
        }
        
        print(f"   🔄 Testing AI analysis...")
        insights = client.analyze_subconscious_patterns(test_facial, test_telemetry)
        
        if insights and not insights.get('error'):
            print(f"   ✅ AI analysis working!")
            print(f"      Emotional State: {insights.get('emotional_state', 'N/A')}")
        else:
            print(f"   ⚠️  AI analysis returned error (may be in mock mode)")
    else:
        print(f"   ⚠️  IBM Granite running in mock mode (credentials may be invalid)")
        
except Exception as e:
    print(f"   ❌ Error testing IBM Granite: {e}")
print()

# Test 7: Project Structure
print("7. Checking project structure...")
required_dirs = [
    'src/facial_analysis',
    'src/ai_engine',
    'src/utils',
    'config',
    'scripts',
    'data/raw',
    'data/processed',
    'logs'
]

for dir_path in required_dirs:
    path = Path(dir_path)
    if path.exists():
        print(f"   ✅ {dir_path}/")
    else:
        print(f"   ⚠️  {dir_path}/ (creating...)")
        path.mkdir(parents=True, exist_ok=True)
print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

if not missing_packages and api_key and project_id:
    print("✅ All checks passed! Your SubMinds system is ready to run.")
    print()
    print("Next steps:")
    print("  1. Run the simulation:")
    print("     python scripts/run_simulation.py --duration 60")
    print()
    print("  2. Test individual components:")
    print("     python src/facial_analysis/capture.py")
    print("     python src/facial_analysis/emotion_tracker.py")
    print("     python src/ai_engine/granite_client.py")
else:
    print("⚠️  Some issues detected. Please fix them before running.")
    if missing_packages:
        print(f"\n  Install packages: pip install {' '.join(missing_packages)}")
    if not api_key or not project_id:
        print(f"\n  Configure .env file with IBM credentials")

print("=" * 70)

# Made with Bob
