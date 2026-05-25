"""
Facial expression detection using DeepFace
"""
from typing import Dict, Any, Optional
import numpy as np
from deepface import DeepFace

from ..utils.logger import get_logger

logger = get_logger(__name__)


class ExpressionDetector:
    """Detect facial expressions and emotions"""
    
    # Emotion labels
    EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def __init__(self, model_name: str = "Emotion"):
        """
        Initialize expression detector
        
        Args:
            model_name: DeepFace model to use for emotion detection
        """
        self.model_name = model_name
        logger.info(f"Initializing ExpressionDetector with model: {model_name}")
        
        # Pre-load model
        try:
            DeepFace.build_model(model_name)
            logger.info("Expression detection model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
            
    def detect_emotion(
        self,
        frame: np.ndarray,
        face_bbox: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Detect emotion in a frame
        
        Args:
            frame: Input frame (BGR format)
            face_bbox: Optional face bounding box to focus analysis
            
        Returns:
            Dictionary containing emotion analysis results
        """
        try:
            # Analyze frame
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # Extract emotion data
            if isinstance(result, list):
                result = result[0]
                
            emotions = result.get('emotion', {})
            dominant_emotion = result.get('dominant_emotion', 'neutral')
            
            # Calculate valence and arousal
            valence = self._calculate_valence(emotions)
            arousal = self._calculate_arousal(emotions)
            
            return {
                'emotions': emotions,
                'dominant_emotion': dominant_emotion,
                'confidence': emotions.get(dominant_emotion, 0.0),
                'valence': valence,
                'arousal': arousal,
                'all_emotions': emotions
            }
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return {
                'emotions': {emotion: 0.0 for emotion in self.EMOTIONS},
                'dominant_emotion': 'neutral',
                'confidence': 0.0,
                'valence': 0.0,
                'arousal': 0.0,
                'error': str(e)
            }
            
    def _calculate_valence(self, emotions: Dict[str, float]) -> float:
        """
        Calculate valence (negative to positive) from emotions
        
        Args:
            emotions: Dictionary of emotion scores
            
        Returns:
            Valence score from -1 (negative) to 1 (positive)
        """
        # Positive emotions
        positive = emotions.get('happy', 0) + emotions.get('surprise', 0) * 0.5
        
        # Negative emotions
        negative = (
            emotions.get('angry', 0) +
            emotions.get('sad', 0) +
            emotions.get('fear', 0) +
            emotions.get('disgust', 0)
        )
        
        # Normalize to [-1, 1]
        total = positive + negative
        if total > 0:
            valence = (positive - negative) / total
        else:
            valence = 0.0
            
        return valence
        
    def _calculate_arousal(self, emotions: Dict[str, float]) -> float:
        """
        Calculate arousal (calm to excited) from emotions
        
        Args:
            emotions: Dictionary of emotion scores
            
        Returns:
            Arousal score from 0 (calm) to 1 (excited)
        """
        # High arousal emotions
        high_arousal = (
            emotions.get('angry', 0) +
            emotions.get('fear', 0) +
            emotions.get('surprise', 0) +
            emotions.get('happy', 0) * 0.7
        )
        
        # Low arousal emotions
        low_arousal = (
            emotions.get('sad', 0) +
            emotions.get('neutral', 0) +
            emotions.get('disgust', 0) * 0.5
        )
        
        # Normalize to [0, 1]
        total = high_arousal + low_arousal
        if total > 0:
            arousal = high_arousal / total
        else:
            arousal = 0.5  # neutral arousal
            
        return arousal
        
    def detect_micro_expression(
        self,
        frame_sequence: list,
        threshold: float = 0.3
    ) -> Optional[Dict[str, Any]]:
        """
        Detect micro-expressions from a sequence of frames
        
        Args:
            frame_sequence: List of consecutive frames
            threshold: Minimum emotion change to detect micro-expression
            
        Returns:
            Micro-expression data or None
        """
        if len(frame_sequence) < 3:
            return None
            
        try:
            # Analyze first and last frames
            first_emotion = self.detect_emotion(frame_sequence[0])
            last_emotion = self.detect_emotion(frame_sequence[-1])
            
            # Check for significant emotion change
            first_dom = first_emotion['dominant_emotion']
            last_dom = last_emotion['dominant_emotion']
            
            if first_dom != last_dom:
                # Calculate emotion change magnitude
                change = abs(
                    first_emotion['emotions'][last_dom] -
                    last_emotion['emotions'][last_dom]
                )
                
                if change >= threshold:
                    return {
                        'detected': True,
                        'from_emotion': first_dom,
                        'to_emotion': last_dom,
                        'change_magnitude': change,
                        'duration_frames': len(frame_sequence)
                    }
                    
        except Exception as e:
            logger.error(f"Error detecting micro-expression: {e}")
            
        return None
        
    def calculate_stress_level(self, emotions: Dict[str, float]) -> float:
        """
        Calculate stress level from emotions
        
        Args:
            emotions: Dictionary of emotion scores
            
        Returns:
            Stress level from 0 (no stress) to 10 (high stress)
        """
        # Stress indicators
        stress_emotions = {
            'angry': 1.0,
            'fear': 1.0,
            'disgust': 0.7,
            'sad': 0.5
        }
        
        stress_score = sum(
            emotions.get(emotion, 0) * weight
            for emotion, weight in stress_emotions.items()
        )
        
        # Normalize to 0-10 scale
        stress_level = min(stress_score / 10.0, 1.0) * 10
        
        return stress_level


# Example usage
if __name__ == "__main__":
    import cv2
    from ..utils.logger import setup_logger
    
    setup_logger(__name__, level="DEBUG")
    
    detector = ExpressionDetector()
    
    # Test with webcam
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Detect emotion
            result = detector.detect_emotion(frame)
            
            logger.info(
                f"Emotion: {result['dominant_emotion']} "
                f"({result['confidence']:.2f}), "
                f"Valence: {result['valence']:.2f}, "
                f"Arousal: {result['arousal']:.2f}"
            )
            
            # Display
            cv2.putText(
                frame,
                f"{result['dominant_emotion']} ({result['confidence']:.2f})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            cv2.imshow('Expression Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Made with Bob
