# SubMinds Quick Start Guide

Get up and running with SubMinds in 5 minutes!

---

## 🚀 Quick Installation

### Option 1: Local Setup (Recommended for Development)

```bash
# 1. Clone and navigate
git clone <repository-url>
cd subminds-may-2026

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies (this resolves ALL import errors)
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your IBM credentials (see below)

# 5. Set Python path
export PYTHONPATH=$(pwd)/src  # Windows: set PYTHONPATH=%CD%\src

# 6. Run!
python scripts/run_simulation.py
```

### Option 2: Docker Setup (Recommended for Production)

```bash
# 1. Clone and navigate
git clone <repository-url>
cd subminds-may-2026

# 2. Set up environment
cp .env.example .env
# Edit .env with your credentials

# 3. Build and run
docker-compose up --build

# 4. View logs
docker-compose logs -f subminds
```

---

## 🔑 Getting IBM Granite API Keys

### Quick Steps:

1. **Sign up**: Go to [IBM Cloud](https://cloud.ibm.com/registration)
2. **Create service**: Search for "Watson Machine Learning" → Create
3. **Get credentials**: Service Credentials → New credential → Copy API key
4. **Create project**: Watson Studio → Create project → Copy Project ID
5. **Add to .env**:
   ```env
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_PROJECT_ID=your_project_id_here
   ```

**Detailed guide**: See `docs/IBM_GRANITE_SETUP.md`

---

## ✅ Verify Installation

Run this to check if everything is working:

```bash
python -c "
import cv2
import mediapipe
import numpy
from deepface import DeepFace
from ibm_watson_machine_learning.foundation_models import Model
print('✅ All imports successful!')
"
```

---

## 🐛 Fixing Import Errors

**All import errors are resolved by installing dependencies:**

```bash
pip install -r requirements.txt
```

This single command installs:
- ✅ opencv-python (cv2)
- ✅ mediapipe
- ✅ numpy
- ✅ deepface
- ✅ ibm-watson-machine-learning
- ✅ python-dotenv
- ✅ pyyaml
- ✅ And 50+ other packages

**Still having issues?** See `docs/INSTALLATION.md` for detailed troubleshooting.

---

## 📁 Project Structure

```
subminds-may-2026/
├── src/                    # Source code
│   ├── facial_analysis/    # Facial expression detection
│   ├── ai_engine/          # IBM Granite integration
│   └── utils/              # Utilities
├── config/                 # Configuration files
├── scripts/                # Executable scripts
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── Dockerfile             # Docker configuration
```

---

## 🎯 What SubMinds Does

1. **Captures** your facial expressions via webcam (30 FPS)
2. **Detects** 7 emotions: happy, sad, angry, fear, surprise, disgust, neutral
3. **Tracks** stress levels, valence, and arousal over time
4. **Analyzes** patterns using IBM Granite AI
5. **Predicts** optimal mental states for peak performance

---

## 🔧 Common Commands

```bash
# Run simulation
python scripts/run_simulation.py

# Run with Docker
docker-compose up

# Stop Docker
docker-compose down

# View logs
tail -f logs/simulation.log

# Test imports
python -c "from src.utils import setup_logger; print('OK')"

# Install in development mode
pip install -e .
```

---

## 📚 Next Steps

1. ✅ **Complete setup**: Follow installation steps above
2. ✅ **Get IBM keys**: See `docs/IBM_GRANITE_SETUP.md`
3. ✅ **Run simulation**: `python scripts/run_simulation.py`
4. ✅ **Read docs**: Check `README.md`, `SOLUTION.md`, `IMPLEMENTATION_GUIDE.md`
5. ✅ **Integrate TORCS**: See `gym_torcs/README.md`

---

## 🆘 Getting Help

### Documentation
- **Installation**: `docs/INSTALLATION.md`
- **IBM Setup**: `docs/IBM_GRANITE_SETUP.md`
- **Architecture**: `SOLUTION.md`
- **Implementation**: `IMPLEMENTATION_GUIDE.md`

### Troubleshooting
- **Import errors**: Run `pip install -r requirements.txt`
- **Camera issues**: Check `docs/INSTALLATION.md` → Troubleshooting
- **IBM auth fails**: Verify credentials in `.env`
- **Docker issues**: Ensure Docker is running

---

## 💡 Pro Tips

1. **Use virtual environment** to avoid dependency conflicts
2. **Set PYTHONPATH** to resolve import issues
3. **Check .gitignore** - never commit `.env` file!
4. **Monitor IBM usage** to avoid unexpected costs
5. **Use Docker** for consistent deployment

---

## 🎉 You're Ready!

SubMinds is now set up and ready to analyze subconscious decision-making patterns!

**Start the simulation:**
```bash
python scripts/run_simulation.py
```

**Questions?** Check the documentation or create an issue on GitHub.

---

*SubMinds - Understanding the subconscious mind of champions* 🏎️🧠