# SubMinds Quick Start Guide
## Your System is Configured and Ready!

---

## ✅ Your IBM Configuration

**Project ID**: `c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf`  
**API Key**: `XRNJls6GZurytauCdeC1T0sTIRMyViF9KvSDvCM86MSC`  
**Region**: EU-GB (Europe - Great Britain)  
**URL**: `https://eu-gb.ml.cloud.ibm.com`  
**Project Name**: "sub"  
**Created**: 2026-05-25

✅ **All credentials are configured in `.env` and `config/ibm_granite_config.yaml`**

---

## 🚀 Run Your System NOW!

### Step 1: Install Dependencies (First Time Only)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all packages
pip install -r requirements.txt
```

### Step 2: Verify Setup

```powershell
# Run verification script
python test_setup.py
```

Expected output:
```
✅ All checks passed! Your SubMinds system is ready to run.
```

### Step 3: Run SubMinds!

```powershell
# Run for 60 seconds
python scripts/run_simulation.py --duration 60

# Or run indefinitely (Ctrl+C to stop)
python scripts/run_simulation.py
```

---

## 📊 What Will Happen

When you run the simulation:

1. **Webcam activates** - Captures your face at 30 FPS
2. **Emotion detection** - Analyzes your facial expressions
3. **IBM Granite AI** - Generates psychological insights every 2 seconds
4. **Real-time logging** - Shows progress in console
5. **Statistics** - Final report when you stop

### Expected Console Output:

```
============================================================
SubMinds - Subconscious Decision Analysis for F1 Drivers
============================================================
Start Time: 2026-05-25 13:00:00
Duration: 60s
============================================================

INFO - SubMinds simulation initialized
INFO - Initializing components...
INFO - Camera 0 initialized successfully
INFO - IBM Granite AI client initialized
INFO - All components initialized successfully
INFO - Simulation started. Press Ctrl+C to stop.
INFO - Progress: 1.0s | Frames: 30 | FPS: 30.0 | Emotion: neutral | Insights: 0
INFO - AI Insights: Driver showing neutral emotion with valence 0.00
INFO - Progress: 2.0s | Frames: 60 | FPS: 30.0 | Emotion: happy | Insights: 1
...
```

---

## 🧪 Test Individual Components

### Test Webcam Capture
```powershell
python src/facial_analysis/capture.py
```

### Test Emotion Detection
```powershell
python src/facial_analysis/emotion_tracker.py
```

### Test IBM Granite AI
```powershell
python src/ai_engine/granite_client.py
```

---

## 📁 Your Project Structure

```
subminds-may-2026/
├── .env                          ✅ Your IBM credentials
├── config/
│   ├── ibm_granite_config.yaml  ✅ IBM Granite config
│   ├── camera_config.yaml       ✅ Webcam settings
│   └── database_config.yaml     ⚠️  Optional (for later)
├── src/
│   ├── facial_analysis/
│   │   ├── capture.py           ✅ Webcam capture
│   │   └── emotion_tracker.py   ✅ Emotion detection
│   ├── ai_engine/
│   │   └── granite_client.py    ✅ IBM Granite AI
│   └── utils/
│       ├── logger.py            ✅ Logging
│       └── config_loader.py     ✅ Config management
├── scripts/
│   └── run_simulation.py        ✅ Main runner
├── test_setup.py                ✅ Verification script
└── logs/                        📝 Auto-created logs
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Camera not found"
```powershell
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"

# Update camera_id in config/camera_config.yaml if needed
```

### Issue: "IBM Granite authentication failed"
- Your credentials are already configured in `.env`
- If you see errors, verify the API key is still valid at: https://cloud.ibm.com/
- The system will run in mock mode if IBM is unavailable

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `QUICK_START.md` | This file - Quick reference |
| `COMPLETE_SETUP_GUIDE.md` | Detailed installation guide |
| `IBM_WATSON_STUDIO_GUIDE.md` | IBM resources & templates |
| `ADAPT_IOT_TO_SUBMINDS.md` | IoT template adaptation |
| `README.md` | Project overview |
| `IMPLEMENTATION_GUIDE.md` | Technical implementation |

---

## 🎯 Next Steps After Running

### 1. Import IBM Watson Studio IoT Template

```
1. Go to: https://dataplatform.cloud.ibm.com/
2. Click "Import project"
3. Enter Project ID: c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf
4. Follow ADAPT_IOT_TO_SUBMINDS.md guide
```

### 2. Analyze Your Data

```powershell
# Check logs
Get-Content logs\simulation.log -Tail 50

# View captured data
dir data\raw\
```

### 3. Extend Functionality

- Add TORCS racing simulation integration
- Implement art psychology analysis
- Create real-time dashboard with Dash/Streamlit
- Add database storage for long-term analysis

---

## ✨ Your System Features

✅ **Real-time facial capture** at 30 FPS  
✅ **7 emotion categories** (happy, sad, angry, fear, surprise, disgust, neutral)  
✅ **Valence & arousal** calculation  
✅ **IBM Granite AI** integration with your credentials  
✅ **Comprehensive logging** to files and console  
✅ **Statistics tracking** for all components  
✅ **Error handling** with graceful degradation  
✅ **Mock modes** for testing without dependencies  

---

## 🎉 You're Ready!

Your SubMinds system is **fully configured** with your IBM credentials and ready to run!

**Start now:**
```powershell
python scripts/run_simulation.py --duration 60
```

---

## 📞 Support Resources

- **IBM Watson Studio**: https://dataplatform.cloud.ibm.com/
- **Your Project**: https://dataplatform.cloud.ibm.com/projects/c01ebe61-c1ef-4f7d-9706-2da1b4c01fcf
- **IBM Granite Docs**: https://www.ibm.com/granite
- **DeepFace**: https://github.com/serengil/deepface
- **MediaPipe**: https://google.github.io/mediapipe/

---

🏎️🧠 **SubMinds - Understanding the subconscious mind of champions!**

*Your system is configured and ready. Just run it!*