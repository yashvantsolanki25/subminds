# SubMinds Implementation Guide

This guide provides detailed instructions, code templates, and configuration files needed to implement the SubMinds project.

---

## 📦 Dependencies & Requirements

### Python Requirements (requirements.txt)

```txt
# Core Dependencies
python>=3.9

# TORCS Integration
gym==0.21.0
numpy==1.24.3
opencv-python==4.8.0

# Computer Vision & Facial Analysis
mediapipe==0.10.3
deepface==0.0.79
tensorflow==2.13.0
keras==2.13.1
mtcnn==0.1.1

# Image Processing & Art Analysis
Pillow==10.0.0
scikit-image==0.21.0
matplotlib==3.7.2
seaborn==0.12.2

# IBM Watson & AI
ibm-watson-machine-learning==1.0.327
ibm-cloud-sdk-core==3.16.7
requests==2.31.0

# Data Processing
pandas==2.0.3
scipy==1.11.1

# Database
psycopg2-binary==2.9.7
pymongo==4.4.1
sqlalchemy==2.0.19

# Web Framework & Dashboard
fastapi==0.101.0
uvicorn==0.23.2
dash==2.12.1
plotly==5.16.1
streamlit==1.25.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
python-multipart==0.0.6
websockets==11.0.3

# Testing
pytest==7.4.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Development
black==23.7.0
flake8==6.1.0
mypy==1.4.1
```

---

## 🔧 Configuration Files

### 1. IBM Granite Configuration (config/ibm_granite_config.yaml)

```yaml
# IBM Granite AI Configuration
ibm_granite:
  # IBM Cloud Credentials
  api_key: "${IBM_CLOUD_API_KEY}"  # Set via environment variable
  url: "https://us-south.ml.cloud.ibm.com"
  project_id: "${IBM_PROJECT_ID}"
  
  # Model Configuration
  model:
    id: "ibm/granite-13b-chat-v2"
    version: "latest"
  
  # Generation Parameters
  parameters:
    max_tokens: 2000
    temperature: 0.7
    top_p: 0.9
    top_k: 50
    repetition_penalty: 1.1
    
  # Rate Limiting
  rate_limits:
    requests_per_minute: 60
    tokens_per_minute: 100000
    retry_attempts: 3
    retry_delay: 2
    
  # Caching
  cache:
    enabled: true
    ttl: 3600  # seconds
    max_size: 1000
```

### 2. TORCS Configuration (config/torcs_config.yaml)

```yaml
# TORCS Environment Configuration
torcs:
  # Server Settings
  server:
    host: "localhost"
    port: 3101
    vision_port: 3102
    
  # Environment Settings
  environment:
    vision: true
    throttle: true
    gear_change: false
    
  # Track Settings
  track:
    name: "aalborg"
    category: "road"
    
  # Race Settings
  race:
    mode: "practice"
    laps: 10
    damage: false
    fuel: false
    
  # Performance Settings
  performance:
    max_steps: 10000
    terminal_judge_start: 500
    termination_limit_progress: 5
    default_speed: 50
```

### 3. Camera Configuration (config/camera_config.yaml)

```yaml
# Webcam Capture Configuration
camera:
  # Device Settings
  device:
    id: 0  # Default webcam
    width: 1280
    height: 720
    fps: 30
    
  # Face Detection
  face_detection:
    model: "mediapipe"
    min_detection_confidence: 0.7
    min_tracking_confidence: 0.5
    max_num_faces: 1
    
  # Recording Settings
  recording:
    enabled: true
    format: "mp4"
    codec: "mp4v"
    save_path: "data/raw/video"
    
  # Buffer Settings
  buffer:
    max_size: 1000  # frames
    flush_interval: 60  # seconds
```

### 4. Database Configuration (config/database_config.yaml)

```yaml
# Database Configuration
database:
  # PostgreSQL (Structured Data)
  postgresql:
    host: "${POSTGRES_HOST:localhost}"
    port: 5432
    database: "subminds"
    user: "${POSTGRES_USER}"
    password: "${POSTGRES_PASSWORD}"
    pool_size: 10
    max_overflow: 20
    
  # MongoDB (Unstructured Data)
  mongodb:
    host: "${MONGO_HOST:localhost}"
    port: 27017
    database: "subminds"
    user: "${MONGO_USER}"
    password: "${MONGO_PASSWORD}"
    auth_source: "admin"
    
  # Redis (Caching)
  redis:
    host: "${REDIS_HOST:localhost}"
    port: 6379
    db: 0
    password: "${REDIS_PASSWORD}"
```

---

## 🏗️ Project Structure Setup

### Directory Creation Script (scripts/setup_environment.sh)

```bash
#!/bin/bash
# SubMinds Environment Setup Script

echo "Setting up SubMinds project structure..."

# Create main directories
mkdir -p subminds-may-2026/{config,src,data,tests,docs,notebooks,scripts}

# Create source subdirectories
mkdir -p subminds-may-2026/src/{facial_analysis,art_analysis,torcs_integration,ai_engine,database,dashboard,utils}

# Create data subdirectories
mkdir -p subminds-may-2026/data/{raw,processed,models,art_samples}
mkdir -p subminds-may-2026/data/raw/{video,telemetry,expressions}

# Create __init__.py files
touch subminds-may-2026/src/__init__.py
touch subminds-may-2026/src/facial_analysis/__init__.py
touch subminds-may-2026/src/art_analysis/__init__.py
touch subminds-may-2026/src/torcs_integration/__init__.py
touch subminds-may-2026/src/ai_engine/__init__.py
touch subminds-may-2026/src/database/__init__.py
touch subminds-may-2026/src/dashboard/__init__.py
touch subminds-may-2026/src/utils/__init__.py
touch subminds-may-2026/tests/__init__.py

# Create .env template
cat > subminds-may-2026/.env.example << 'EOF'
# IBM Cloud Credentials
IBM_CLOUD_API_KEY=your_api_key_here
IBM_PROJECT_ID=your_project_id_here

# Database Credentials
POSTGRES_HOST=localhost
POSTGRES_USER=subminds
POSTGRES_PASSWORD=your_password_here

MONGO_HOST=localhost
MONGO_USER=subminds
MONGO_PASSWORD=your_password_here

REDIS_HOST=localhost
REDIS_PASSWORD=your_password_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
EOF

echo "Project structure created successfully!"
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your credentials"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Set up databases (see docs/installation.md)"
```

---

## 💻 Core Implementation Templates

### 1. Facial Analysis Module (src/facial_analysis/capture.py)

```python
"""
Webcam capture module for facial expression analysis
"""
import cv2
import mediapipe as mp
import time
import threading
from collections import deque
from typing import Optional, Dict, Any
import numpy as np


class FacialCaptureModule:
    """Captures and processes facial expressions from webcam"""
    
    def __init__(self, camera_id: int = 0, fps: int = 30, buffer_size: int = 1000):
        """
        Initialize facial capture module
        
        Args:
            camera_id: Camera device ID
            fps: Target frames per second
            buffer_size: Maximum buffer size for frames
        """
        self.camera_id = camera_id
        self.fps = fps
        self.buffer_size = buffer_size
        
        # Initialize camera
        self.camera = cv2.VideoCapture(camera_id)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.7
        )
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Buffer for captured frames
        self.buffer = deque(maxlen=buffer_size)
        
        # Threading
        self.is_capturing = False
        self.capture_thread = None
        
    def start_capture(self):
        """Start capturing frames in a separate thread"""
        if not self.is_capturing:
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.start()
            
    def stop_capture(self):
        """Stop capturing frames"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()
            
    def _capture_loop(self):
        """Main capture loop (runs in separate thread)"""
        while self.is_capturing:
            ret, frame = self.camera.read()
            if ret:
                timestamp = time.time()
                
                # Detect faces
                faces = self._detect_faces(frame)
                
                # Get facial landmarks
                landmarks = self._get_landmarks(frame) if faces else None
                
                # Store in buffer
                self.buffer.append({
                    'timestamp': timestamp,
                    'frame': frame,
                    'faces': faces,
                    'landmarks': landmarks
                })
                
            # Control frame rate
            time.sleep(1.0 / self.fps)
            
    def _detect_faces(self, frame: np.ndarray) -> list:
        """Detect faces in frame using MediaPipe"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                faces.append({
                    'bbox': {
                        'x': bbox.xmin,
                        'y': bbox.ymin,
                        'width': bbox.width,
                        'height': bbox.height
                    },
                    'confidence': detection.score[0]
                })
        return faces
        
    def _get_landmarks(self, frame: np.ndarray) -> Optional[Dict]:
        """Extract facial landmarks using MediaPipe Face Mesh"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            return {
                'landmarks': [
                    {'x': lm.x, 'y': lm.y, 'z': lm.z}
                    for lm in landmarks.landmark
                ]
            }
        return None
        
    def get_current_frame(self) -> Optional[Dict[str, Any]]:
        """Get the most recent captured frame"""
        return self.buffer[-1] if self.buffer else None
        
    def get_frame_history(self, n: int = 100) -> list:
        """Get last n frames from buffer"""
        return list(self.buffer)[-n:]
        
    def release(self):
        """Release camera resources"""
        self.stop_capture()
        self.camera.release()
        self.face_detection.close()
        self.face_mesh.close()


# Example usage
if __name__ == "__main__":
    capture = FacialCaptureModule(camera_id=0, fps=30)
    capture.start_capture()
    
    try:
        while True:
            frame_data = capture.get_current_frame()
            if frame_data:
                print(f"Captured frame at {frame_data['timestamp']}")
                print(f"Faces detected: {len(frame_data['faces'])}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping capture...")
    finally:
        capture.release()
```

### 2. IBM Granite Client (src/ai_engine/granite_client.py)

```python
"""
IBM Granite AI Client for pattern analysis
"""
import os
import yaml
from typing import Dict, Any, List, Optional
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams


class GraniteAIClient:
    """Client for IBM Granite AI model"""
    
    def __init__(self, config_path: str = "config/ibm_granite_config.yaml"):
        """
        Initialize Granite AI client
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.model = self._initialize_model()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Replace environment variables
        api_key = os.getenv('IBM_CLOUD_API_KEY')
        project_id = os.getenv('IBM_PROJECT_ID')
        
        if not api_key or not project_id:
            raise ValueError("IBM_CLOUD_API_KEY and IBM_PROJECT_ID must be set")
            
        config['ibm_granite']['api_key'] = api_key
        config['ibm_granite']['project_id'] = project_id
        
        return config['ibm_granite']
        
    def _initialize_model(self) -> Model:
        """Initialize IBM Granite model"""
        credentials = {
            "url": self.config['url'],
            "apikey": self.config['api_key']
        }
        
        model_id = self.config['model']['id']
        project_id = self.config['project_id']
        
        parameters = {
            GenParams.MAX_NEW_TOKENS: self.config['parameters']['max_tokens'],
            GenParams.TEMPERATURE: self.config['parameters']['temperature'],
            GenParams.TOP_P: self.config['parameters']['top_p'],
            GenParams.TOP_K: self.config['parameters']['top_k'],
        }
        
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=project_id
        )
        
        return model
        
    def analyze_subconscious_patterns(
        self,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any],
        art_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze subconscious patterns using multimodal data
        
        Args:
            facial_data: Facial expression analysis results
            telemetry: Racing telemetry data
            art_analysis: Optional art psychology analysis
            
        Returns:
            Dictionary containing insights and recommendations
        """
        prompt = self._create_analysis_prompt(facial_data, telemetry, art_analysis)
        
        response = self.model.generate_text(prompt=prompt)
        
        insights = self._parse_response(response)
        
        return insights
        
    def _create_analysis_prompt(
        self,
        facial_data: Dict,
        telemetry: Dict,
        art_analysis: Optional[Dict]
    ) -> str:
        """Create analysis prompt for Granite"""
        
        prompt = f"""You are an expert sports psychologist analyzing F1 driver performance.

FACIAL EXPRESSION DATA:
- Dominant emotion: {facial_data.get('dominant_emotion', 'unknown')}
- Stress level: {facial_data.get('stress_level', 0)}/10
- Valence (negative to positive): {facial_data.get('valence', 0)}
- Arousal (calm to excited): {facial_data.get('arousal', 0)}

RACING TELEMETRY:
- Speed: {telemetry.get('speed', 0)} km/h
- Steering angle: {telemetry.get('steering', 0)}
- Track position: {telemetry.get('track_position', 0)}
- Lap time: {telemetry.get('lap_time', 0)}

"""
        
        if art_analysis:
            prompt += f"""ART PSYCHOLOGY ANALYSIS:
- Dominant colors: {art_analysis.get('dominant_colors', [])}
- Composition style: {art_analysis.get('composition_style', 'unknown')}
- Psychological themes: {art_analysis.get('themes', [])}

"""
        
        prompt += """Based on this multimodal data, provide:
1. Current subconscious emotional state and its impact on performance
2. Identified stress triggers and coping mechanisms
3. Decision-making patterns (conscious vs subconscious)
4. Specific recommendations for mental state optimization
5. Predictive indicators for performance changes

Format your response as structured JSON."""
        
        return prompt
        
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Granite response into structured insights"""
        # TODO: Implement robust JSON parsing
        # For now, return raw response
        return {
            'raw_response': response,
            'timestamp': time.time()
        }


# Example usage
if __name__ == "__main__":
    client = GraniteAIClient()
    
    facial_data = {
        'dominant_emotion': 'focused',
        'stress_level': 6,
        'valence': 0.3,
        'arousal': 0.7
    }
    
    telemetry = {
        'speed': 180,
        'steering': -0.3,
        'track_position': 0.1,
        'lap_time': 95.3
    }
    
    insights = client.analyze_subconscious_patterns(facial_data, telemetry)
    print(insights)
```

---

## 🚀 Quick Start Guide

### Step 1: Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd subminds-may-2026

# Run setup script
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

### Step 3: Database Setup

```bash
# Start PostgreSQL
sudo service postgresql start

# Create database
createdb subminds

# Run migrations (after implementing)
python scripts/init_database.py
```

### Step 4: IBM Granite Setup

1. Create IBM Cloud account at https://cloud.ibm.com
2. Create Watson Machine Learning service
3. Get API key and project ID
4. Add credentials to `.env` file

### Step 5: TORCS Setup

```bash
# Install TORCS (see gym_torcs/README.md)
cd gym_torcs
# Follow installation instructions

# Test TORCS
python example_experiment.py
```

### Step 6: Run SubMinds

```bash
# Start the system
python scripts/run_simulation.py

# Or run dashboard
streamlit run src/dashboard/app.py
```

---

## 📚 Additional Documentation

See the `docs/` directory for:
- `installation.md` - Detailed installation guide
- `ibm_granite_setup.md` - IBM Granite configuration
- `usage.md` - Usage instructions
- `api_reference.md` - API documentation
- `architecture.md` - System architecture details

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_facial_analysis.py

# Run with coverage
pytest --cov=src tests/
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Camera not detected
```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

**Issue**: IBM Granite authentication fails
- Verify API key in `.env`
- Check IBM Cloud service status
- Ensure Watson ML service is active

**Issue**: TORCS connection timeout
- Verify TORCS is running
- Check port 3101 is not blocked
- Run `sh autostart.sh` manually

---

## 📞 Support

For issues and questions:
1. Check documentation in `docs/`
2. Review troubleshooting section
3. Contact project team

---

*This implementation guide will be continuously updated as the project evolves.*