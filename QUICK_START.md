# SubMinds Desktop - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
# Run the installation script (PowerShell)
.\install_and_run.ps1

# OR manually install
pip install -r requirements.txt
```

### Step 2: Configure Your Credentials
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your IBM Cloud credentials:
   ```
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_PROJECT_ID=your_project_id_here
   ```

**Get IBM Cloud Credentials:**
- Sign up at https://cloud.ibm.com/
- Create a Watson Studio project
- Get API key from IBM Cloud dashboard
- Copy project ID from Watson Studio

### Step 3: Run the Application
```bash
# Windows - Double click:
run_subminds.bat

# OR run with Python:
python subminds_desktop.py
```

## 📱 Using the Application

### Main Interface
- **Start Analysis** - Begin facial expression monitoring
- **Configure** - Set up IBM credentials and camera
- **Clear Output** - Clear the analysis window
- **Export Results** - Save analysis to file

### Status Indicators
- 🟢 Green = Working
- 🟡 Yellow = Mock mode (no IBM credentials)
- 🔴 Red = Not available

### First Time Setup
1. Click **Configure** button
2. Enter your IBM Cloud API Key
3. Enter your IBM Project ID
4. Set Camera ID (0 for default webcam)
5. Click **Save**
6. Click **Start Analysis**

## 🔧 Troubleshooting

### Camera Not Working?
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```
Then update `CAMERA_ID` in `.env`

### IBM Granite Not Working?
- App works in mock mode without credentials
- Check your API key and project ID in `.env`
- Verify internet connection
- Live Granite requires `ibm-watson-machine-learning`, which may not install on Python 3.14.
- Use Python 3.11 and install the IBM package for live model support.

### Module Errors?
```bash
pip install -r requirements.txt --force-reinstall
```

## 📊 What You'll See

The application will show:
- Real-time emotional state analysis
- Stress level monitoring
- AI-powered recommendations
- Performance statistics

## 🎯 Next Steps

1. ✅ Install and run the application
2. ✅ Configure IBM Cloud credentials
3. ✅ Start your first analysis session
4. ✅ Review the insights and recommendations
5. ✅ Export results for further analysis

## 💡 Tips

- **No IBM Credentials?** The app works in mock mode for testing
- **Privacy:** All processing is local, only AI analysis uses IBM Cloud
- **Camera:** Make sure to allow camera access when prompted
- **Results:** Export regularly to save your analysis data

## 📞 Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---

**Ready to analyze? Run the app and click "Start Analysis"!** 🏎️🧠