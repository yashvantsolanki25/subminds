# SubMinds Installation & Usage Guide

## Quick Start

### 1. Install Dependencies

Run the installation script:
```bash
.\install_dependencies.bat
```

Or manually install:
```bash
pip install opencv-python pillow python-dotenv numpy pyyaml requests
```

### 2. Configure API Keys

The `.env` file is already configured with your IBM Cloud credentials:
- IBM_CLOUD_API_KEY: XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC
- IBM_PROJECT_ID: c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf
- CAMERA_ID: 0 (default laptop camera)
- ANALYSIS_INTERVAL: 2.0 seconds

### 3. Run the Application

```bash
python subminds_app.py
```

## Features

✅ **Camera Capture**: Automatically uses camera 0 (your laptop webcam)
✅ **Face Detection**: Real-time face detection using OpenCV Haar Cascades
✅ **Expression Analysis**: Detects emotions (happy, focused, neutral)
✅ **AI Analysis**: IBM Granite AI integration (mock mode if API unavailable)
✅ **Real-time Display**: Live camera feed with annotations
✅ **Statistics**: FPS, analysis count, uptime tracking

## How to Use

1. **Start the Application**: Run `python subminds_app.py`
2. **Click "Start Analysis"**: This will:
   - Activate your laptop camera (camera 0)
   - Start capturing your face
   - Analyze facial expressions every 2 seconds
   - Display results in real-time
3. **View Results**: 
   - Camera feed shows on the left
   - Analysis output appears on the right
   - Statistics display at the bottom

## Camera Setup

The application is configured to use **Camera ID 0** (your default laptop camera).

- If you have multiple cameras, you can change this in the `.env` file
- The camera will automatically start when you click "Start Analysis"
- Face detection works in real-time with live annotations

## Troubleshooting

### Camera Not Working
- Ensure no other application is using the camera
- Check camera permissions in Windows Settings
- Try changing CAMERA_ID in `.env` file (0, 1, 2, etc.)

### Import Errors
- Run `.\install_dependencies.bat` again
- Verify Python version: `python --version` (should be 3.14)
- Check installed packages: `pip list`

### IBM Watson Warnings
- The app works in mock mode without IBM Watson ML
- Full AI features require pandas which has build issues on Python 3.14
- Consider using Python 3.11 for full IBM Watson integration

## System Requirements

- **Python**: 3.14 (installed)
- **Camera**: Webcam (camera 0)
- **OS**: Windows 11
- **RAM**: 4GB minimum
- **Disk**: 500MB for dependencies

## Package Status

✅ **Installed & Working**:
- opencv-python (4.13.0.92)
- pillow (12.2.0)
- python-dotenv (1.2.2)
- numpy (2.4.6)
- pyyaml (6.0.3)
- requests (2.34.2)

⚠️ **Optional (Not Installed)**:
- ibm-watson-machine-learning (requires pandas with build issues)
- ibm-cloud-sdk-core (requires pandas)

## Application Flow

1. **Initialization**:
   - Loads .env configuration automatically
   - Initializes camera (ID 0)
   - Sets up face detector
   - Connects to IBM Granite (mock mode if unavailable)

2. **Analysis Loop**:
   - Captures frame from camera
   - Detects face using Haar Cascades
   - Analyzes expression (happy/focused/neutral)
   - Sends data to IBM Granite AI
   - Displays insights and recommendations

3. **Real-time Display**:
   - Shows live camera feed
   - Draws face detection boxes
   - Displays emotion labels
   - Updates statistics (FPS, count, uptime)

## Made with Bob - Desktop Edition