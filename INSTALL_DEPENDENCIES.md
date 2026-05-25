# SubMinds - Dependency Installation Guide

## ⚠️ Virtual Environment Creation Failed?

If you got the error `CREATE_VENV.PIP_FAILED_INSTALL_REQUIREMENTS`, follow this manual installation guide.

---

## 🔧 Manual Installation Steps

### Step 1: Create Virtual Environment (Without Auto-Install)

```powershell
# Navigate to project directory
cd c:\Users\Yashv\Downloads\subminds-may-2026

# Create virtual environment manually
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### Step 2: Upgrade pip

```powershell
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel
```

### Step 3: Install Dependencies in Order

Install packages in this specific order to avoid conflicts:

#### 3.1 Core Dependencies
```powershell
pip install numpy==1.24.3
pip install opencv-python==4.8.0.76
```

#### 3.2 TensorFlow and Keras
```powershell
pip install tensorflow==2.13.0
pip install tf-keras==2.13.0
```

#### 3.3 Computer Vision
```powershell
pip install mediapipe==0.10.3
pip install Pillow==10.0.0
```

#### 3.4 DeepFace (May take a while)
```powershell
pip install deepface==0.0.79
```

#### 3.5 IBM Watson
```powershell
pip install ibm-watson-machine-learning==1.0.327
pip install ibm-cloud-sdk-core==3.16.7
```

#### 3.6 Data Processing
```powershell
pip install pandas==2.0.3
pip install scipy==1.11.1
```

#### 3.7 Utilities
```powershell
pip install python-dotenv==1.0.0
pip install pyyaml==6.0.1
pip install requests==2.31.0
```

#### 3.8 Optional (For Dashboard)
```powershell
pip install fastapi==0.101.0
pip install uvicorn==0.23.2
pip install plotly==5.16.1
pip install matplotlib==3.7.2
```

---

## ✅ Verify Installation

```powershell
# Check Python version
python --version

# Verify key packages
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import mediapipe; print('MediaPipe:', mediapipe.__version__)"
python -c "import tensorflow; print('TensorFlow:', tensorflow.__version__)"
python -c "import deepface; print('DeepFace: OK')"
python -c "from ibm_watson_machine_learning.foundation_models import Model; print('IBM WML: OK')"
```

---

## 🚀 Alternative: Install All at Once (May Fail)

If you want to try installing all at once:

```powershell
pip install -r requirements.txt
```

If this fails, go back to the step-by-step installation above.

---

## 🐛 Common Issues

### Issue: TensorFlow Installation Fails

**Solution 1**: Install specific version
```powershell
pip install tensorflow==2.13.0 --no-cache-dir
```

**Solution 2**: Use CPU-only version
```powershell
pip install tensorflow-cpu==2.13.0
```

### Issue: DeepFace Installation Fails

**Solution**: Install dependencies first
```powershell
pip install numpy opencv-python tensorflow
pip install deepface --no-deps
pip install deepface
```

### Issue: MediaPipe Installation Fails

**Solution**: Try without version constraint
```powershell
pip install mediapipe
```

### Issue: IBM Watson ML Installation Fails

**Solution**: Install with no dependencies first
```powershell
pip install ibm-watson-machine-learning --no-deps
pip install ibm-watson-machine-learning
```

---

## 📊 Minimal Installation (For Testing)

If you just want to test the system without all features:

```powershell
# Minimal set
pip install numpy opencv-python python-dotenv pyyaml requests

# Run in mock mode (no AI features)
python scripts/run_simulation.py --duration 30
```

The system will work in "mock mode" without DeepFace and IBM Watson.

---

## ✅ After Installation

Once all packages are installed, run:

```powershell
# Verify setup
python test_setup.py

# Run SubMinds
python scripts/run_simulation.py --duration 60
```

---

## 💡 Pro Tips

1. **Use Python 3.9-3.11**: TensorFlow 2.13 works best with these versions
2. **Install in order**: Follow the step-by-step guide to avoid conflicts
3. **Be patient**: DeepFace and TensorFlow take time to install
4. **Check disk space**: Need at least 5GB free for all packages
5. **Use stable internet**: Large downloads required

---

## 🆘 Still Having Issues?

### Option 1: Use Conda (Alternative)

```powershell
# Create conda environment
conda create -n subminds python=3.10
conda activate subminds

# Install packages
conda install -c conda-forge opencv
conda install -c conda-forge tensorflow
pip install mediapipe deepface ibm-watson-machine-learning python-dotenv pyyaml
```

### Option 2: Use Docker (Advanced)

```powershell
# Build Docker image
docker build -t subminds .

# Run container
docker run -it --device=/dev/video0 subminds
```

### Option 3: Run Without Dependencies

The system has mock modes for all external dependencies. You can run it without installing everything:

```powershell
# Install only core packages
pip install numpy python-dotenv pyyaml

# Run in mock mode
python scripts/run_simulation.py --duration 30
```

---

## 📞 Need Help?

If installation continues to fail:

1. Check Python version: `python --version` (should be 3.9-3.11)
2. Check pip version: `pip --version` (should be 23.0+)
3. Try installing packages one by one
4. Check error messages carefully
5. Ensure you have admin rights if needed

---

**Once installed, your SubMinds system is ready to run!**

```powershell
python scripts/run_simulation.py --duration 60
```

🏎️🧠 *SubMinds - Understanding the subconscious mind of champions!*