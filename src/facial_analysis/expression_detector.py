"""
Facial Expression Detector using OpenCV
Detects faces and analyzes basic expressions
"""
import cv2
import numpy as np
import logging
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class ExpressionDetector:
    """Detects facial expressions using OpenCV"""
    
    def __init__(self):
        """Initialize expression detector with Haar Cascades"""
        self.face_cascade = None
        self.eye_cascade = None
        self.smile_cascade = None
        
        try:
            # Load Haar Cascade classifiers
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.smile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_smile.xml'
            )
            logger.info("Expression detector initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing expression detector: {e}")
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of face rectangles (x, y, w, h)
        """
        if self.face_cascade is None:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces.tolist() if len(faces) > 0 else []
    
    def analyze_expression(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Analyze facial expression in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary with expression analysis
        """
        if self.face_cascade is None:
            return self._get_default_analysis()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        if len(faces) == 0:
            return {
                'face_detected': False,
                'dominant_emotion': 'no_face',
                'confidence': 0.0,
                'valence': 0.0,
                'arousal': 0.0,
                'stress_level': 0
            }
        
        # Get the largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        
        # Extract face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Detect eyes
        eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 5) if self.eye_cascade else []
        
        # Detect smile
        smiles = self.smile_cascade.detectMultiScale(
            face_roi, 1.8, 20, minSize=(25, 25)
        ) if self.smile_cascade else []
        
        # Analyze expression based on features
        has_smile = len(smiles) > 0
        eye_count = len(eyes)
        
        # Calculate face area ratio for stress detection
        face_area = w * h
        frame_area = gray.shape[0] * gray.shape[1]
        face_ratio = face_area / frame_area
        
        # Advanced emotion detection
        if has_smile and eye_count >= 2:
            emotion = 'joyful'
            emotion_desc = 'Happy and engaged - optimal performance state'
            valence = 0.8
            arousal = 0.6
            stress_level = 2
        elif has_smile:
            emotion = 'content'
            emotion_desc = 'Relaxed and positive'
            valence = 0.6
            arousal = 0.4
            stress_level = 3
        elif eye_count >= 2 and face_ratio > 0.15:
            emotion = 'intensely_focused'
            emotion_desc = 'High concentration - peak performance zone'
            valence = 0.4
            arousal = 0.8
            stress_level = 7
        elif eye_count >= 2:
            emotion = 'focused'
            emotion_desc = 'Concentrated and alert'
            valence = 0.3
            arousal = 0.7
            stress_level = 6
        elif eye_count == 1:
            emotion = 'contemplative'
            emotion_desc = 'Thinking deeply or partially distracted'
            valence = 0.2
            arousal = 0.5
            stress_level = 5
        elif face_ratio < 0.08:
            emotion = 'distant'
            emotion_desc = 'Disengaged or looking away'
            valence = -0.1
            arousal = 0.3
            stress_level = 4
        else:
            emotion = 'neutral'
            emotion_desc = 'Calm and composed'
            valence = 0.0
            arousal = 0.5
            stress_level = 5
        
        return {
            'face_detected': True,
            'face_location': (x, y, w, h),
            'dominant_emotion': emotion,
            'emotion_description': emotion_desc,
            'confidence': 0.75 + (0.1 if has_smile else 0.0) + (0.05 if eye_count >= 2 else 0.0),
            'valence': valence,
            'arousal': arousal,
            'stress_level': stress_level,
            'features': {
                'eyes_detected': eye_count,
                'smile_detected': has_smile,
                'face_size_ratio': face_ratio
            },
            'performance_indicators': {
                'engagement_level': 'high' if arousal > 0.6 else 'medium' if arousal > 0.4 else 'low',
                'emotional_stability': 'stable' if abs(valence) < 0.3 else 'positive' if valence > 0 else 'negative',
                'stress_category': 'high' if stress_level > 6 else 'moderate' if stress_level > 4 else 'low'
            }
        }
    
    def draw_annotations(
        self,
        frame: np.ndarray,
        analysis: Dict[str, Any]
    ) -> np.ndarray:
        """
        Draw face detection and analysis on frame
        
        Args:
            frame: Input frame
            analysis: Analysis results
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        if not analysis.get('face_detected', False):
            cv2.putText(
                annotated,
                "No face detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
            return annotated
        
        # Draw face rectangle
        if 'face_location' in analysis:
            x, y, w, h = analysis['face_location']
            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Draw emotion label
            emotion = analysis.get('dominant_emotion', 'unknown')
            confidence = analysis.get('confidence', 0.0)
            label = f"{emotion} ({confidence:.2f})"
            
            cv2.putText(
                annotated,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        return annotated
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis when detector not available"""
        return {
            'face_detected': False,
            'dominant_emotion': 'unknown',
            'confidence': 0.0,
            'valence': 0.0,
            'arousal': 0.0,
            'stress_level': 0
        }
    
    def is_available(self) -> bool:
        """Check if detector is available"""
        return self.face_cascade is not None


# Made with Bob - OpenCV Face Detection
