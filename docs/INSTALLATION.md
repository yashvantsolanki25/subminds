# SubMinds Installation Guide

Complete installation guide for the SubMinds project.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Installation](#local-installation)
3. [Docker Installation](#docker-installation)
4. [Resolving Import Errors](#resolving-import-errors)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- **Python**: 3.9 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 10GB free space
- **Webcam**: Required for facial analysis
- **GPU**: Optional (CUDA-compatible for faster processing)

### Required Accounts
- IBM Cloud account (for Granite AI)
- Git installed
- Docker (optional, for containerized deployment)

---

## Local Installation

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd subminds-may-2026
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will install all required packages including:
- opencv-python (cv2)
- mediapipe
- deepface
- tensorflow
- numpy
- ibm-watson-machine-learning
- pyyaml
- python-dotenv
- And 50+ other dependencies

### Step 5: Set Up Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
# Windows: notepad .env
# Linux/macOS: nano .env
```

Add your credentials:
```env
IBM_CLOUD_API_KEY=your_actual_api_key_here
IBM_PROJECT_ID=your_actual_project_id_here
POSTGRES_PASSWORD=your_secure_password
MONGO_PASSWORD=your_secure_password
```

### Step 6: Create Required Directories

```bash
mkdir -p logs data/raw/video data/processed data/models data/art_samples
```

### Step 7: Set Python Path

**Windows:**
```bash
set PYTHONPATH=%CD%\src
```

**Linux/macOS:**
```bash
export PYTHONPATH=$(pwd)/src
```

Or add to your shell profile:
```bash
echo 'export PYTHONPATH=/path/to/subminds-may-2026/src' >> ~/.bashrc
source ~/.bashrc
```

---

## Docker Installation

### Step 1: Install Docker

**Windows/macOS:**
- Download Docker Desktop from https://www.docker.com/products/docker-desktop

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Step 2: Set Up Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 3: Build Docker Image

```bash
docker-compose build
```

### Step 4: Run with Docker Compose

```bash
docker-compose up -d
```

### Step 5: View Logs

```bash
docker-compose logs -f subminds
```

### Step 6: Stop Services

```bash
docker-compose down
```

---

## Resolving Import Errors

The import errors you see are **expected** before installing dependencies. Here's how to resolve them:

### Error: "Import 'cv2' could not be resolved"

**Solution:**
```bash
pip install opencv-python==4.8.0
```

**Verify:**
```python
python -c "import cv2; print(cv2.__version__)"
```

### Error: "Import 'mediapipe' could not be resolved"

**Solution:**
```bash
pip install mediapipe==0.10.3
```

**Verify:**
```python
python -c "import mediapipe; print('MediaPipe OK')"
```

### Error: "Import 'numpy' could not be resolved"

**Solution:**
```bash
pip install numpy==1.24.3
```

**Verify:**
```python
python -c "import numpy; print(numpy.__version__)"
```

### Error: "Import 'deepface' could not be resolved"

**Solution:**
```bash
pip install deepface==0.0.79
```

**Verify:**
```python
python -c "from deepface import DeepFace; print('DeepFace OK')"
```

### Error: "Import 'ibm_watson_machine_learning' could not be resolved"

**Solution:**
```bash
pip install ibm-watson-machine-learning==1.0.327
```

**Verify:**
```python
python -c "from ibm_watson_machine_learning.foundation_models import Model; print('IBM Watson ML OK')"
```

### Error: "Import 'dotenv' could not be resolved"

**Solution:**
```bash
pip install python-dotenv==1.0.0
```

**Verify:**
```python
python -c "from dotenv import load_dotenv; print('dotenv OK')"
```

### Error: "Import 'yaml' could not be resolved"

**Solution:**
```bash
pip install pyyaml==6.0.1
```

**Verify:**
```python
python -c "import yaml; print('PyYAML OK')"
```

### Install All at Once

Instead of installing individually, run:
```bash
pip install -r requirements.txt
```

This will install all dependencies and resolve all import errors.

---

## Verification

### 1. Verify Python Environment

```bash
python --version  # Should be 3.9+
pip list | grep -E "opencv|mediapipe|deepface|numpy|ibm-watson"
```

### 2. Test Imports

Create a test file `test_imports.py`:
```python
#!/usr/bin/env python3
"""Test all imports"""

print("Testing imports...")

try:
    import cv2
    print("✓ OpenCV (cv2)")
except ImportError as e:
    print(f"✗ OpenCV: {e}")

try:
    import mediapipe
    print("✓ MediaPipe")
except ImportError as e:
    print(f"✗ MediaPipe: {e}")

try:
    import numpy
    print("✓ NumPy")
except ImportError as e:
    print(f"✗ NumPy: {e}")

try:
    from deepface import DeepFace
    print("✓ DeepFace")
except ImportError as e:
    print(f"✗ DeepFace: {e}")

try:
    from ibm_watson_machine_learning.foundation_models import Model
    print("✓ IBM Watson ML")
except ImportError as e:
    print(f"✗ IBM Watson ML: {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv")
except ImportError as e:
    print(f"✗ python-dotenv: {e}")

try:
    import yaml
    print("✓ PyYAML")
except ImportError as e:
    print(f"✗ PyYAML: {e}")

print("\nAll imports successful!" if all else "Some imports failed!")
```

Run it:
```bash
python test_imports.py
```

### 3. Test Project Modules

```bash
# Test utils
python -c "from src.utils import setup_logger, load_config; print('✓ Utils module')"

# Test facial analysis
python -c "from src.facial_analysis import FacialCaptureModule; print('✓ Facial analysis module')"

# Test AI engine
python -c "from src.ai_engine import GraniteAIClient; print('✓ AI engine module')"
```

### 4. Test Configuration Loading

```bash
python -c "from src.utils.config_loader import load_config; config = load_config('camera_config.yaml'); print('✓ Config loaded')"
```

### 5. Run Full System Test

```bash
python scripts/run_simulation.py
```

Expected output:
```
============================================================
SubMinds - Subconscious Decision Analysis
============================================================
INFO - Loading configurations...
INFO - Initializing components...
INFO - All components initialized successfully
INFO - Starting facial capture...
INFO - Simulation running. Press Ctrl+C to stop...
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=$(pwd)/src  # Linux/macOS
set PYTHONPATH=%CD%\src        # Windows
```

### Issue: "Camera not found"

**Solution:**
```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"

# Update camera_config.yaml with correct camera ID
```

### Issue: "Permission denied" on Linux

**Solution:**
```bash
# Add user to video group
sudo usermod -aG video $USER
# Log out and log back in
```

### Issue: "TensorFlow not using GPU"

**Solution:**
```bash
# Install CUDA-enabled TensorFlow
pip uninstall tensorflow
pip install tensorflow-gpu==2.13.0

# Verify GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Issue: "IBM Watson authentication failed"

**Solution:**
1. Verify API key in `.env`
2. Check IBM Cloud service status
3. Ensure Watson ML service is active
4. See `docs/IBM_GRANITE_SETUP.md` for detailed setup

### Issue: "Out of memory"

**Solution:**
```bash
# Reduce buffer sizes in config files
# camera_config.yaml: buffer.max_size: 500
# Or add more RAM/swap space
```

---

## Post-Installation

### 1. Configure IBM Granite

Follow the detailed guide:
```bash
cat docs/IBM_GRANITE_SETUP.md
```

### 2. Set Up Databases (Optional)

If using PostgreSQL and MongoDB:
```bash
# Start with Docker
docker-compose up -d postgres mongodb

# Or install locally
# PostgreSQL: https://www.postgresql.org/download/
# MongoDB: https://www.mongodb.com/try/download/community
```

### 3. Run Tests

```bash
pytest tests/
```

### 4. Start Development

```bash
# Run simulation
python scripts/run_simulation.py

# Or use Docker
docker-compose up
```

---

## Quick Start Commands

```bash
# Complete installation
git clone <repo>
cd subminds-may-2026
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
export PYTHONPATH=$(pwd)/src
python scripts/run_simulation.py
```

---

## Getting Help

- **Documentation**: Check `README.md`, `SOLUTION.md`, `IMPLEMENTATION_GUIDE.md`
- **IBM Setup**: See `docs/IBM_GRANITE_SETUP.md`
- **Issues**: Create an issue on GitHub
- **Community**: Join project discussions

---

**✅ Installation Complete!**

You're now ready to use SubMinds for subconscious decision analysis!