# Quick Start Guide - After API Key Update

## Step 1: Get a Valid API Key

### In IBM Cloud Console:
1. Go to: https://cloud.ibm.com/
2. Log in with your IBM Cloud account
3. Click the avatar/profile icon (top right)
4. Select **"Manage"** → **"Access (IAM)"**
5. In the left sidebar, click **"Users"**
6. Click your username
7. In the **"API keys"** section, click **"Create Classic infrastructure API key"** or **"Create an IBM Cloud API key"**
8. Give it a name (e.g., "SubMinds App")
9. Copy the API key (it will only be shown once)

### For WatsonX Space:
- Verify you have access to Machine Learning service in us-south region
- Space ID: `2239ca43-f17c-433a-b34d-e8a60a817e08` (already configured)

---

## Step 2: Update Your Application

### Edit `.env` file:
```
IBM_CLOUD_API_KEY=<PASTE_YOUR_NEW_API_KEY_HERE>
IBM_SPACE_ID=2239ca43-f17c-433a-b34d-e8a60a817e08
IBM_WATSON_URL=https://us-south.ml.cloud.ibm.com
CAMERA_ID=0
ANALYSIS_INTERVAL=2.0
MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
TEMPERATURE=0.7
TOP_P=0.9
MAX_TOKENS=2000
```

Replace `<PASTE_YOUR_NEW_API_KEY_HERE>` with your actual API key.

---

## Step 3: Verify Setup

Run the test to confirm everything works:
```powershell
python test_watsonx_integration.py
```

Expected output should show:
```
✓ API Key found: RqrZi695xF...
✓ Space ID found: 2239ca43-f17c-433a-b34d-e8a60a817e08
✓ ibm_watsonx_ai.Credentials imported successfully
✓ Credentials object created successfully
✓ ModelInference initialized successfully
✓ GraniteAIClient initialized with active model
```

---

## Step 4: Run the Application

### Desktop App:
```powershell
python subminds_app.py
```

The GUI will open with:
- Camera feed on the left
- Analysis controls on the right
- Real-time output console

### Click "Start Analysis" to begin:
1. Camera feed starts
2. Facial expressions detected
3. Granite AI analyzes expressions
4. Results appear in output panel
5. Click "Stop Analysis" to finish

---

## Features Available

### Camera & Analysis
- ✓ Real-time video feed
- ✓ Facial expression detection
- ✓ Expression emotion tracking
- ✓ Pattern analysis with Granite AI
- ✓ Auto-save screenshots

### Controls
- **Start Analysis** - Begin camera and AI analysis
- **Stop Analysis** - Pause and stop
- **Configure** - Update API key and settings
- **Save Snapshot** - Capture current frame
- **Open Captures** - View saved images
- **Export CSV** - Export session data

### System Status
Real-time indicators for:
- 🟢 Camera Status
- 🟢 IBM Granite Status
- 🟢 Analysis Status
- Session Statistics (analyses, uptime, FPS)

---

## Common Issues & Solutions

### Issue: "API key could not be found"
**Solution:** 
- Generate a new API key in IBM Cloud console
- Paste it into `.env` file
- Restart the application

### Issue: "Camera not accessible"
**Solution:**
- Check webcam is plugged in
- Change CAMERA_ID in `.env` (try 1, 2, 3 for external cameras)
- Run: `python test_camera_and_api.py`

### Issue: "Connection timeout"
**Solution:**
- Check internet connection
- Verify Watson URL in `.env` is correct
- Check IBM Cloud service status

### Issue: App runs but Granite shows "mock mode"
**Solution:**
- API key is invalid or expired
- Get a new API key from IBM Cloud console
- Update `.env` file
- Restart app

---

## Testing Without API Key (Demo Mode)

The application works in **mock mode** even without a valid API key:
- ✓ Camera feed displays
- ✓ Facial expressions detected
- ✓ Interface fully functional
- ⚠ AI analysis will be simulated (not real Granite responses)

Perfect for testing the UI!

---

## Important Files

| File | Purpose |
|------|---------|
| `.env` | Your credentials (NEVER commit to git) |
| `subminds_app.py` | Main desktop application |
| `watsonx_analysis.py` | Direct WatsonX API examples |
| `config/ibm_granite_config.yaml` | AI model settings |
| `test_watsonx_integration.py` | Verify your setup |

---

## Tips for Best Results

### Performance
- Close other applications to free up camera resources
- Use good lighting for better face detection
- Keep your face in view of camera

### Analysis Quality
- Maintain steady expressions for 2+ seconds
- Let expressions show naturally
- Don't cover face with hands
- Ensure camera is at eye level

### Data Collection
- Run multiple sessions for better pattern analysis
- Export CSV data for offline analysis
- Screenshot interesting expressions
- Keep notes on external factors (mood, stress, etc.)

---

## Support & Resources

- **IBM Cloud Dashboard**: https://cloud.ibm.com/
- **Watson Machine Learning Docs**: https://cloud.ibm.com/docs/machine-learning
- **WatsonX.ai**: https://www.ibm.com/watsonx
- **Granite Model**: https://github.com/ibm-granite

---

## Next Steps

1. ✓ Get valid API key from IBM Cloud
2. ✓ Update `.env` file
3. ✓ Run `test_watsonx_integration.py` 
4. ✓ Launch `python subminds_app.py`
5. ✓ Click "Start Analysis"
6. ✓ Enjoy subconscious pattern insights!

---

Your SubMinds application is ready! 🚀
