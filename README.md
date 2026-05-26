# SubMinds - Desktop Application
**Subconscious Decision Analysis for F1 Drivers**

**Version:** 1.0.0 - Desktop Edition  
**Target Date:** May 2026  
**Status:** Active Development

## 🎯 Project Overview

SubMinds is a desktop application that analyzes the subconscious decision-making patterns of F1 drivers using:
- **Real-time facial expression analysis** via webcam
- **IBM Granite AI** for deep pattern recognition and psychological insights
- **Behavioral prediction models** for performance optimization
- **Desktop GUI** built with Python Tkinter

## 🖥️ Desktop Application Features

### Real-Time Analysis Dashboard
- Live facial expression monitoring
- Emotion tracking and stress level detection
- AI-powered insights and recommendations
- Performance statistics and metrics

### Easy Configuration
- Simple GUI-based configuration
- Environment variable support via .env file
- No complex deployment needed

### Offline Capability
- Works with or without IBM Granite AI
- Mock mode for testing and development
- Local data processing

## 📋 System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** 3.9 or higher
- **Webcam:** For facial expression capture
- **IBM Cloud Account:** (Optional) For AI-powered analysis

## 🚀 Quick Start Guide

### 1. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Configure the Application

Copy the example environment file and add your credentials:

```bash
# Copy the example file
copy .env.example .env

# Edit .env with your credentials
# - IBM_CLOUD_API_KEY: Your IBM Cloud API key
# - IBM_PROJECT_ID: Your IBM Watson Studio project ID
```

**Get IBM Cloud Credentials:**
1. Sign up at https://cloud.ibm.com/
2. Create a Watson Studio project
3. Get your API key from IBM Cloud dashboard
4. Copy your project ID from Watson Studio

### 3. Run the Application

```bash
# Start the desktop application
python subminds_desktop.py
```

## 📖 How to Use

### Starting Analysis

1. **Launch the Application**
   - Run `python subminds_desktop.py`
   - The main window will appear

2. **Configure Settings** (First Time)
   - Click "Configure" button
   - Enter your IBM Cloud API Key
   - Enter your IBM Project ID
   - Set Camera ID (0 for default webcam)
   - Click "Save"

3. **Start Analysis**
   - Click "Start Analysis" button
   - Allow camera access when prompted
   - Analysis will begin automatically

4. **View Results**
   - Real-time insights appear in the output panel
   - Status indicators show system health
   - Statistics update automatically

### Controls

- **Start/Stop Analysis:** Begin or pause the analysis
- **Configure:** Open settings dialog
- **Clear Output:** Clear the analysis output window
- **Export Results:** Save analysis results to file

### Status Indicators

- 🟢 **Green:** Component working normally
- 🟡 **Yellow:** Component in mock/fallback mode
- 🔴 **Red:** Component not available

## 🔧 Configuration Options

### Environment Variables (.env file)

```bash
# IBM Cloud Credentials
IBM_CLOUD_API_KEY=your_api_key_here
IBM_PROJECT_ID=your_project_id_here

# Camera Settings
CAMERA_ID=0                    # 0 = default webcam

# Analysis Settings
ANALYSIS_INTERVAL=2.0          # Seconds between analyses
LOG_LEVEL=INFO                 # Logging level
```

### Camera Configuration

- **CAMERA_ID=0:** Default built-in webcam
- **CAMERA_ID=1:** External USB webcam
- **CAMERA_ID=2:** Second external camera

## 📁 Project Structure

```
subminds-may-2026/
├── subminds_desktop.py          # Main desktop application
├── requirements.txt             # Python dependencies
├── .env.example                 # Example configuration
├── .env                         # Your configuration (create this)
├── README.md                    # This file
├── setup.py                     # Package setup
├── config/                      # Configuration files
│   ├── camera_config.yaml
│   ├── database_config.yaml
│   └── torcs_config.yaml
└── src/                         # Source code
    ├── ai_engine/               # IBM Granite AI integration
    │   ├── granite_client.py
    │   └── pattern_recognition.py
    ├── facial_analysis/         # Facial expression analysis
    │   ├── capture.py
    │   ├── emotion_tracker.py
    │   └── expression_detector.py
    └── utils/                   # Utility functions
        ├── config_loader.py
        └── logger.py
```

## 🎨 Features in Detail

### Facial Expression Analysis
- Captures driver facial expressions via webcam
- Detects emotions: focus, stress, confidence, anxiety
- Tracks emotional state changes in real-time
- Correlates expressions with performance

### IBM Granite AI Integration
- Advanced pattern recognition
- Psychological insights generation
- Performance predictions
- Personalized recommendations

### Desktop Interface
- Clean, intuitive GUI
- Real-time status monitoring
- Easy configuration management
- Export capabilities

## 🔒 Privacy & Security

- All data processed locally on your machine
- IBM Cloud credentials stored in .env file (never committed to git)
- Webcam access only when analysis is running
- No data sent to external servers (except IBM Granite API)

## 🐛 Troubleshooting

### Camera Not Working
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"

# Try different CAMERA_ID in .env file
CAMERA_ID=1
```

### IBM Granite Not Available
- Application works in mock mode without IBM credentials
- Check your API key and project ID
- Verify internet connection
- Check IBM Cloud service status

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Check tkinter installation
python -c "import tkinter"
```

## 📊 Understanding the Output

### Analysis Results Format
```
[HH:MM:SS] Analysis Results:
  Emotional State: Driver showing focused emotion with valence 0.30
  Stress Analysis: Moderate stress levels detected. Monitor for changes.
  Recommendations:
    • Maintain current mental state
    • Focus on breathing exercises
    • Monitor stress triggers
```

### Statistics Panel
- **Total Analyses:** Number of completed analyses
- **Success Rate:** Percentage of successful analyses
- **Avg Response Time:** Average time per analysis
- **Uptime:** How long the system has been running

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Backing Up Data
- Export results regularly using "Export Results" button
- Keep your .env file secure and backed up

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the .env.example file for configuration help
3. Ensure all dependencies are installed correctly

## 🎯 Roadmap

- [x] Desktop GUI application
- [x] IBM Granite AI integration
- [x] Facial expression analysis
- [ ] Art psychology analysis module
- [ ] TORCS racing simulation integration
- [ ] Advanced visualization dashboard
- [ ] Multi-driver comparison
- [ ] Historical data analysis

## 📄 License

[To be determined]

---

**SubMinds Desktop Edition** - Understanding the subconscious mind of champions 🏎️🧠

*Made with Bob - Desktop Edition*