# SubMinds - Subconscious Decision Analysis for F1 Drivers

**Project Name:** SubMinds  
**Version:** 1.0.0  
**Target Date:** May 2026  
**Status:** Planning Phase

## 🎯 Project Overview

SubMinds is an innovative AI-powered system that analyzes the subconscious decision-making patterns of F1 drivers by combining:
- **Real-time facial expression analysis** during TORCS racing simulations
- **Art analysis** of driver-created drawings and designs
- **IBM Granite AI** for deep pattern recognition and psychological insights
- **Behavioral prediction models** for performance optimization

## 🧠 The Problem (Our Magic Solution)

### The Challenge
F1 drivers make split-second decisions under extreme pressure, often relying on subconscious patterns developed through years of training. Traditional performance analysis focuses on:
- Lap times and telemetry data
- Conscious decision-making processes
- Post-race interviews and debriefs

**What's Missing:** The subconscious emotional and psychological states that influence critical racing decisions.

### Our Magic Solution
SubMinds bridges this gap by:

1. **Facial Expression Monitoring**: Captures micro-expressions during TORCS simulations via webcam
2. **Art Psychology Analysis**: Analyzes driver-created artwork to understand deeper psychological patterns
3. **AI-Powered Insights**: Uses IBM Granite to correlate subconscious signals with racing performance
4. **Predictive Modeling**: Identifies patterns that predict optimal vs. suboptimal decision-making

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SubMinds Platform                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Webcam     │    │  TORCS Sim   │    │  Art Upload  │  │
│  │   Capture    │    │  Environment │    │   Module     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                    │           │
│         └───────────────────┼────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │   Data Collection & Synchronization    │           │
│         └───────────────────┬────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │      Facial Expression Analysis        │           │
│         │    (OpenCV + DeepFace + MediaPipe)     │           │
│         └───────────────────┬────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │        Art Psychology Analysis         │           │
│         │   (Color, Composition, Symbolism)      │           │
│         └───────────────────┬────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │         IBM Granite AI Engine          │           │
│         │  (Pattern Recognition & Correlation)   │           │
│         └───────────────────┬────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │    Subconscious Pattern Database       │           │
│         │  (Driver Profiles & Insights Storage)  │           │
│         └───────────────────┬────────────────────┘           │
│                             │                                │
│         ┌───────────────────▼────────────────────┐           │
│         │    Real-time Dashboard & Insights      │           │
│         │   (Visualization & Recommendations)    │           │
│         └────────────────────────────────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features

### 1. Real-Time Facial Expression Analysis
- Captures driver facial expressions during TORCS simulation
- Detects micro-expressions: stress, focus, confidence, anxiety
- Correlates expressions with racing events (overtaking, braking, cornering)
- Tracks emotional state changes throughout race sessions

### 2. Art Psychology Module
- Analyzes driver-created artwork (drawings, designs, sketches)
- Extracts psychological insights from:
  - Color choices and patterns
  - Composition and spatial relationships
  - Symbolic elements and themes
  - Drawing pressure and stroke patterns
- Builds long-term psychological profiles

### 3. IBM Granite AI Integration
- Advanced pattern recognition across multimodal data
- Correlates subconscious signals with performance metrics
- Identifies hidden decision-making patterns
- Generates actionable insights for driver improvement

### 4. Performance Prediction
- Predicts optimal mental states for peak performance
- Identifies stress triggers and anxiety patterns
- Recommends pre-race mental preparation strategies
- Tracks improvement over time

## 📋 Technical Stack

### Core Technologies
- **Simulation**: TORCS (gym_torcs environment)
- **Computer Vision**: OpenCV, MediaPipe, DeepFace
- **AI/ML**: IBM Granite, TensorFlow, PyTorch
- **Art Analysis**: PIL, scikit-image, custom algorithms
- **Backend**: Python 3.9+, FastAPI
- **Database**: PostgreSQL, MongoDB
- **Visualization**: Plotly, Dash, Streamlit

### Key Libraries
```python
- gym_torcs          # Racing simulation environment
- opencv-python      # Video capture and processing
- mediapipe          # Facial landmark detection
- deepface           # Emotion recognition
- ibm-watson-machine-learning  # IBM Granite integration
- tensorflow         # Deep learning models
- numpy, pandas      # Data processing
- plotly, dash       # Interactive visualizations
```

## 📁 Project Structure

```
subminds-may-2026/
├── README.md                    # This file
├── ISSUE.md                     # Problem statement
├── SOLUTION.md                  # Detailed solution architecture
├── requirements.txt             # Python dependencies
├── setup.py                     # Installation script
├── config/
│   ├── ibm_granite_config.yaml  # IBM Granite API configuration
│   ├── torcs_config.yaml        # TORCS environment settings
│   └── camera_config.yaml       # Webcam capture settings
├── src/
│   ├── __init__.py
│   ├── facial_analysis/
│   │   ├── __init__.py
│   │   ├── capture.py           # Webcam capture module
│   │   ├── expression_detector.py  # Facial expression analysis
│   │   └── emotion_tracker.py   # Real-time emotion tracking
│   ├── art_analysis/
│   │   ├── __init__.py
│   │   ├── image_processor.py   # Art image processing
│   │   ├── color_analyzer.py    # Color psychology analysis
│   │   ├── composition_analyzer.py  # Composition analysis
│   │   └── psychological_insights.py  # Art psychology engine
│   ├── torcs_integration/
│   │   ├── __init__.py
│   │   ├── environment.py       # TORCS environment wrapper
│   │   ├── telemetry.py         # Racing telemetry capture
│   │   └── synchronizer.py      # Data synchronization
│   ├── ai_engine/
│   │   ├── __init__.py
│   │   ├── granite_client.py    # IBM Granite API client
│   │   ├── pattern_recognition.py  # Pattern detection
│   │   ├── correlation_engine.py   # Multi-modal correlation
│   │   └── predictor.py         # Performance prediction
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # Database models
│   │   └── repository.py        # Data access layer
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── app.py               # Dashboard application
│   │   ├── visualizations.py    # Chart components
│   │   └── insights_panel.py    # Insights display
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Logging utilities
│       └── validators.py        # Data validation
├── data/
│   ├── raw/                     # Raw captured data
│   ├── processed/               # Processed datasets
│   ├── models/                  # Trained ML models
│   └── art_samples/             # Driver artwork samples
├── tests/
│   ├── __init__.py
│   ├── test_facial_analysis.py
│   ├── test_art_analysis.py
│   ├── test_torcs_integration.py
│   └── test_ai_engine.py
├── docs/
│   ├── installation.md          # Installation guide
│   ├── ibm_granite_setup.md     # IBM Granite setup
│   ├── usage.md                 # Usage instructions
│   ├── api_reference.md         # API documentation
│   └── architecture.md          # Detailed architecture
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   ├── model_training.ipynb
│   └── visualization_examples.ipynb
└── scripts/
    ├── setup_environment.sh     # Environment setup
    ├── run_simulation.py        # Run simulation
    └── train_models.py          # Model training
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- TORCS installed (see gym_torcs documentation)
- Webcam for facial capture
- IBM Cloud account (for Granite AI access)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd subminds-may-2026
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure IBM Granite**
```bash
# Follow docs/ibm_granite_setup.md for detailed instructions
cp config/ibm_granite_config.yaml.example config/ibm_granite_config.yaml
# Edit with your IBM Cloud credentials
```

4. **Setup TORCS**
```bash
cd gym_torcs
# Follow gym_torcs/README.md for TORCS installation
```

5. **Run the system**
```bash
python scripts/run_simulation.py
```

## 📊 Usage Example

```python
from src.torcs_integration import TorcsEnvironment
from src.facial_analysis import FacialAnalyzer
from src.art_analysis import ArtAnalyzer
from src.ai_engine import GraniteClient

# Initialize components
env = TorcsEnvironment(vision=True)
facial_analyzer = FacialAnalyzer(camera_id=0)
art_analyzer = ArtAnalyzer()
granite = GraniteClient(config_path='config/ibm_granite_config.yaml')

# Start simulation with facial tracking
facial_analyzer.start_capture()
observation = env.reset()

# Run simulation loop
for step in range(1000):
    # Get facial expression data
    expression_data = facial_analyzer.get_current_expression()
    
    # Get racing telemetry
    action = agent.act(observation)
    observation, reward, done, info = env.step(action)
    
    # Analyze with IBM Granite
    insights = granite.analyze_subconscious_patterns(
        facial_data=expression_data,
        telemetry=info,
        timestamp=step
    )
    
    if done:
        break

# Analyze driver artwork
art_insights = art_analyzer.analyze_artwork('data/art_samples/driver_drawing.jpg')

# Generate comprehensive report
report = granite.generate_driver_profile(
    session_data=env.get_session_data(),
    facial_history=facial_analyzer.get_history(),
    art_analysis=art_insights
)

print(report)
```

## 🎨 Art Analysis Features

The art analysis module examines driver-created artwork to extract psychological insights:

### Color Psychology
- **Warm colors** (red, orange, yellow): Energy, aggression, confidence
- **Cool colors** (blue, green, purple): Calmness, focus, control
- **Dark tones**: Stress, pressure, intensity
- **Bright tones**: Optimism, clarity, positive mindset

### Composition Analysis
- **Centered compositions**: Balanced, controlled mindset
- **Dynamic angles**: Risk-taking, aggressive approach
- **Symmetry**: Perfectionism, attention to detail
- **Chaos**: Stress, overwhelm, need for support

### Symbolic Elements
- **Speed lines**: Focus on velocity, time pressure
- **Barriers/walls**: Perceived obstacles, limitations
- **Open spaces**: Freedom, confidence, flow state
- **Repetitive patterns**: Obsessive focus, dedication

## 📈 Expected Outcomes

1. **Driver Performance Optimization**
   - 15-20% improvement in stress management
   - Better identification of optimal mental states
   - Personalized pre-race preparation strategies

2. **Subconscious Pattern Recognition**
   - Identify hidden decision-making triggers
   - Predict performance dips before they occur
   - Understand emotional responses to racing scenarios

3. **Long-term Development**
   - Track psychological growth over seasons
   - Identify areas for mental training
   - Build comprehensive driver psychological profiles

## 🔒 Privacy & Ethics

- All data is anonymized and encrypted
- Drivers have full control over their data
- Art analysis is optional and consent-based
- Insights are used solely for performance improvement
- Complies with GDPR and data protection regulations

## 🤝 Contributing

This project is currently in the planning phase. Contributions will be welcome once the initial implementation is complete.

## 📄 License

[To be determined]

## 📞 Contact

For questions or collaboration inquiries, please contact the project team.

## 🗓️ Project Timeline

- **Phase 1 (Months 1-2)**: Core infrastructure and TORCS integration
- **Phase 2 (Months 3-4)**: Facial analysis and art analysis modules
- **Phase 3 (Months 5-6)**: IBM Granite integration and pattern recognition
- **Phase 4 (Months 7-8)**: Dashboard and visualization
- **Phase 5 (Months 9-10)**: Testing and validation
- **Phase 6 (Months 11-12)**: Deployment and documentation

**Target Completion**: May 2026

---

*SubMinds - Understanding the subconscious mind of champions* 🏎️🧠