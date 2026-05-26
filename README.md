# SubMinds — Subconscious Decision Analysis for F1 Drivers

**Version:** 1.0.0 — Desktop Edition  
**Target Date:** May 2026  
**Status:** Active Development  
**Primary App File:** `subminds_app.py`

---

## What is SubMinds?

SubMinds is a Python desktop application that reads the **subconscious mind of F1 drivers in real time**. It combines live webcam facial analysis with IBM Granite AI to detect emotional states, stress patterns, and decision-making tendencies — all while the driver is behind the wheel.

The app captures your face every 2 seconds, runs it through OpenCV-based expression detection, and sends the results to IBM Granite 13B for deep psychological insight generation. Everything runs locally on your machine with no complex deployment.

---

## The Problem SubMinds Solves

### The Hidden Performance Gap in Motorsport

Modern F1 teams have access to thousands of telemetry data points per second — throttle, brake, steering angle, tyre temperature, fuel load. Yet one critical variable remains almost entirely unmeasured:

> **What is happening inside the driver's mind?**

This gap creates real, measurable problems:

| Problem | Impact |
|---|---|
| **Invisible stress buildup** | Drivers accumulate cognitive load lap after lap with no objective measurement. By the time it shows in lap times, it's already too late. |
| **Subconscious decision drift** | Under pressure, drivers make micro-decisions that deviate from their optimal style — aggressive braking, hesitation in corners — without being consciously aware of it. |
| **No emotion-to-performance correlation** | Teams cannot connect emotional state data to lap time data because emotional state data simply doesn't exist in a structured form. |
| **Post-session guesswork** | Debrief sessions rely on driver self-reporting, which is inherently unreliable. Drivers cannot accurately recall their mental state at Turn 7 on Lap 23. |
| **One-size-fits-all coaching** | Mental coaching is generic because there is no per-driver, per-session emotional baseline to work from. |
| **Stress spike blindness** | A sudden stress spike before a critical overtake attempt is invisible to the team. The driver may not even notice it consciously. |

### What SubMinds Does About It

SubMinds creates a **continuous, objective emotional telemetry stream** that runs alongside physical telemetry. It detects:

- Real-time dominant emotion (focused, joyful, stressed, contemplative, distant, neutral)
- Valence score (negative → positive emotional state, -1.0 to +1.0)
- Arousal score (calm → highly activated, 0.0 to 1.0)
- Stress level (0–10 scale, updated every 2 seconds)
- Eye engagement and smile detection via Haar Cascade classifiers
- Stress trend over time (increasing / stable / decreasing)
- Decision pattern analysis (aggressive vs. hesitant driving tendencies)
- Emotion-to-performance correlation (when enough data is collected)

IBM Granite AI then synthesizes all of this into human-readable psychological insights, specific recommendations, and predictive indicators — delivered live to the desktop dashboard.

---

## How the App Works (Technical Overview)

```
Webcam Feed (OpenCV)
       │
       ▼
ExpressionDetector (Haar Cascades)
  - Face detection
  - Eye detection
  - Smile detection
  - Emotion classification
  - Valence / Arousal / Stress scoring
       │
       ▼
GraniteAIClient (IBM Granite 13B)
  - Multimodal prompt construction
  - Subconscious pattern analysis
  - JSON-structured insight generation
  - Mock mode fallback (no credentials needed)
       │
       ▼
SubMindsApp GUI (Tkinter + PIL)
  - Live 640×480 camera feed with face annotations
  - Real-time analysis output panel
  - Status indicators (Camera / IBM Granite / Analysis)
  - Statistics bar (analyses count, uptime, FPS)
  - Snapshot and capture management
```

**Threading model:** The camera feed runs on its own thread at ~30 FPS. The analysis loop runs on a separate thread, firing every 2 seconds (configurable). The GUI thread stays responsive throughout.

**Capture pipeline:** Every analysis cycle saves a timestamped `.jpg` to the `captures/` folder (`analysis_YYYYMMDD_HHMMSS_microseconds.jpg`), creating a full visual record of the session.

---

## Run the App

The file that runs the application is:

```bash
python subminds_app.py
```

This is the complete, production-ready desktop app with:
- Live camera feed embedded in the GUI
- Face detection annotations overlaid on the video
- Full analysis output panel
- Snapshot saving
- Configuration dialog
- Status indicators

> `subminds_app_modern.py` is an alternative dark-theme UI variant. `subminds_desktop.py` is an older, simpler version. **Use `subminds_app.py` for the full experience.**

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Core packages installed: `opencv-python`, `Pillow`, `numpy`, `python-dotenv`, `pyyaml`, `requests`

### 2. Configure Credentials (Optional)

IBM Granite AI is optional. The app runs in mock mode without it.

```bash
copy .env.example .env
```

Edit `.env`:

```bash
IBM_CLOUD_API_KEY=your_api_key_here
IBM_PROJECT_ID=your_project_id_here
CAMERA_ID=0
ANALYSIS_INTERVAL=2.0
```

Get IBM credentials at [cloud.ibm.com](https://cloud.ibm.com/) → Watson Studio → API Key.

### 3. Launch

```bash
python subminds_app.py
```

---

## System Requirements

| Requirement | Minimum |
|---|---|
| OS | Windows 10/11, macOS, Linux |
| Python | 3.9 or higher |
| Webcam | Any USB or built-in camera |
| IBM Cloud | Optional (mock mode available) |

---

## Application Layout

The GUI is split into two columns:

**Left — Camera Panel**
- Live webcam feed at 640×480
- Green bounding box around detected face
- Emotion label + confidence score overlaid
- Timestamp and analysis count on frame
- Controls: Start Analysis, Stop Analysis, Configure, Save Snapshot, Open Captures

**Right — Analysis Panel**
- System status indicators (Camera / IBM Granite / Analysis)
- Scrollable analysis output with timestamped entries
- Each entry shows: emotional state, stress analysis, decision patterns, AI recommendations, predictions, and the saved image filename

**Bottom — Statistics Bar**
- Total analyses performed
- Session uptime
- Camera FPS

---

## Configuration Options

All settings live in `.env`:

```bash
IBM_CLOUD_API_KEY=         # IBM Cloud API key
IBM_PROJECT_ID=            # Watson Studio project ID
CAMERA_ID=0                # 0 = default webcam, 1 = external USB
ANALYSIS_INTERVAL=2.0      # Seconds between AI analyses
LOG_LEVEL=INFO
```

You can also change settings at runtime via the **Configure** button in the app.

---

## Project Structure

```
subminds-may-2026/
├── subminds_app.py              ← MAIN APP — run this
├── subminds_app_modern.py       ← Dark theme UI variant
├── subminds_desktop.py          ← Older simplified version
├── requirements.txt
├── .env.example
├── .env                         ← Your credentials (create from .env.example)
├── setup.py
├── captures/                    ← Auto-saved analysis frames (JPG)
├── config/
│   ├── ibm_granite_config.yaml  ← Granite model parameters
│   ├── camera_config.yaml
│   ├── database_config.yaml
│   └── torcs_config.yaml
└── src/
    ├── ai_engine/
    │   ├── granite_client.py        ← IBM Granite 13B integration + mock mode
    │   └── pattern_recognition.py  ← Stress, decision, micro-expression patterns
    ├── facial_analysis/
    │   ├── capture.py               ← OpenCV webcam capture
    │   ├── expression_detector.py   ← Haar Cascade face/eye/smile detection
    │   └── emotion_tracker.py       ← Emotion history, trends, averages
    └── utils/
        ├── config_loader.py
        └── logger.py
```

---

## Understanding the Analysis Output

Each analysis cycle produces a structured entry:

```
============================================================
[14:32:07] Analysis #12
============================================================
📷 Image: analysis_20260526_143207_482910.jpg

😊 Emotional State: Driver showing intensely_focused emotion with valence 0.40
💪 Stress Analysis: Moderate stress levels detected. Monitor for changes.

🧠 Decision Patterns:
   • Consistent decision-making at 178.3 km/h
   • No hesitation patterns detected

💡 AI Recommendations:
   ✓ Maintain current mental state
   ✓ Focus on breathing exercises
   ✓ Monitor stress triggers

🔮 Predictions:
   → Performance likely to remain stable
   → Watch for stress spike in next 3 laps

============================================================
```

### Emotion Classifications

| Emotion | Trigger Condition | Valence | Stress |
|---|---|---|---|
| `joyful` | Smile + both eyes detected | 0.8 | 2 |
| `content` | Smile only | 0.6 | 3 |
| `intensely_focused` | Both eyes + large face area | 0.4 | 7 |
| `focused` | Both eyes detected | 0.3 | 6 |
| `contemplative` | One eye detected | 0.2 | 5 |
| `distant` | Small face area | -0.1 | 4 |
| `neutral` | Face detected, no features | 0.0 | 5 |

---

## Troubleshooting

### Camera not working
```bash
python -c "import cv2; print([i for i in range(5) if cv2.VideoCapture(i).isOpened()])"
```
Try setting `CAMERA_ID=1` in `.env` if camera 0 fails.

### IBM Granite not connecting
The app automatically falls back to mock mode. Check your API key and project ID in `.env`. Verify your IBM Cloud region matches the URL in `config/ibm_granite_config.yaml` (default: `eu-gb`).

### Module import errors
```bash
pip install -r requirements.txt --force-reinstall
```

### App won't start
```bash
python --version        # Must be 3.9+
python -c "import tkinter"
python -c "import cv2"
python -c "from PIL import Image"
```

### IBM Watson ML install issues (Python 3.12+)
The `ibm-watson-machine-learning` package has known compatibility issues with Python 3.12+. The app runs fully in mock mode without it. If you need live Granite, use Python 3.11.

---

## Privacy & Security

- All video processing happens locally on your machine
- Frames are saved only to the local `captures/` folder
- IBM credentials are stored in `.env` which is `.gitignore`d
- The only external network call is to IBM Granite API (when configured)
- Webcam is only accessed while analysis is running

---

## Roadmap

- [x] Desktop GUI with live camera feed
- [x] OpenCV facial expression detection
- [x] IBM Granite AI integration with mock fallback
- [x] Emotion history tracking and trend analysis
- [x] Pattern recognition engine (stress, decision, micro-expression)
- [ ] TORCS racing simulation integration (telemetry from real sim)
- [ ] Art psychology analysis module
- [ ] Historical session comparison dashboard
- [ ] Multi-driver side-by-side analysis
- [ ] Export to CSV / PDF report

---

## License

To be determined.

---

**SubMinds Desktop Edition** — Understanding the subconscious mind of champions 🏎️🧠
