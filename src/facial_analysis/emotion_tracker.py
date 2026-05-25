"""
Real-time emotion tracking module
Production-ready implementation with comprehensive error handling
"""
import time
import logging
from typing import Dict, Any, List, Optional
from collections import deque
import numpy as np

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    logging.warning("DeepFace not available. Emotion detection will be limited.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmotionTracker:
    """Track emotions over time with smoothing and trend analysis"""
    
    EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def __init__(
        self,
        history_size: int = 100,
        smoothing_window: int = 5,
        confidence_threshold: float = 0.5
    ):
        """
        Initialize emotion tracker
        
        Args:
            history_size: Number of emotion readings to keep in history
            smoothing_window: Window size for moving average smoothing
            confidence_threshold: Minimum confidence for emotion detection
        """
        self.history_size = history_size
        self.smoothing_window = smoothing_window
        self.confidence_threshold = confidence_threshold
        
        # Emotion history
        self.emotion_history: deque = deque(maxlen=history_size)
        
        # Statistics
        self.total_detections = 0
        self.failed_detections = 0
        
        # Check DeepFace availability
        if not DEEPFACE_AVAILABLE:
            logger.warning("DeepFace not installed. Install with: pip install deepface")
    
    def detect_emotion(
        self,
        frame: np.ndarray,
        enforce_detection: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Detect emotion in a frame
        
        Args:
            frame: Input frame (BGR format)
            enforce_detection: Whether to enforce face detection
            
        Returns:
            Dictionary containing emotion data or None if detection fails
        """
        if not DEEPFACE_AVAILABLE:
            return self._get_mock_emotion()
        
        try:
            # Analyze frame with DeepFace
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=enforce_detection,
                detector_backend='opencv',
                silent=True
            )
            
            # Handle both single face and multiple faces
            if isinstance(result, list):
                result = result[0] if result else None
            
            if result is None:
                self.failed_detections += 1
                return None
            
            # Extract emotion data
            emotions = result.get('emotion', {})
            dominant_emotion = result.get('dominant_emotion', 'neutral')
            
            # Calculate confidence
            confidence = emotions.get(dominant_emotion, 0.0) / 100.0
            
            # Check confidence threshold
            if confidence < self.confidence_threshold:
                logger.debug(f"Low confidence detection: {confidence:.2f}")
            
            emotion_data = {
                'timestamp': time.time(),
                'dominant_emotion': dominant_emotion,
                'confidence': confidence,
                'all_emotions': emotions,
                'valence': self._calculate_valence(emotions),
                'arousal': self._calculate_arousal(emotions)
            }
            
            # Add to history
            self.emotion_history.append(emotion_data)
            self.total_detections += 1
            
            return emotion_data
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            self.failed_detections += 1
            return None
    
    def _calculate_valence(self, emotions: Dict[str, float]) -> float:
        """
        Calculate valence (negative to positive emotion)
        
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
        
        # Normalize to -1 to 1
        total = positive + negative
        if total == 0:
            return 0.0
        
        valence = (positive - negative) / total
        return float(np.clip(valence, -1.0, 1.0))
    
    def _calculate_arousal(self, emotions: Dict[str, float]) -> float:
        """
        Calculate arousal (calm to excited)
        
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
        
        # Normalize to 0 to 1
        total = high_arousal + low_arousal
        if total == 0:
            return 0.5
        
        arousal = high_arousal / total
        return float(np.clip(arousal, 0.0, 1.0))
    
    def get_smoothed_emotion(self, window: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get smoothed emotion over recent history
        
        Args:
            window: Window size for smoothing (uses default if None)
            
        Returns:
            Smoothed emotion data or None if insufficient history
        """
        if not self.emotion_history:
            return None
        
        window = window or self.smoothing_window
        recent = list(self.emotion_history)[-window:]
        
        if not recent:
            return None
        
        # Average all emotion scores
        emotion_sums = {emotion: 0.0 for emotion in self.EMOTIONS}
        valence_sum = 0.0
        arousal_sum = 0.0
        
        for data in recent:
            emotions = data['all_emotions']
            for emotion in self.EMOTIONS:
                emotion_sums[emotion] += emotions.get(emotion, 0.0)
            valence_sum += data['valence']
            arousal_sum += data['arousal']
        
        count = len(recent)
        
        # Calculate averages
        avg_emotions = {
            emotion: score / count
            for emotion, score in emotion_sums.items()
        }
        
        # Find dominant emotion
        dominant = max(avg_emotions.items(), key=lambda x: x[1])
        
        return {
            'timestamp': time.time(),
            'dominant_emotion': dominant[0],
            'confidence': dominant[1] / 100.0,
            'all_emotions': avg_emotions,
            'valence': valence_sum / count,
            'arousal': arousal_sum / count,
            'window_size': count
        }
    
    def get_emotion_trend(self, duration: float = 60.0) -> Dict[str, Any]:
        """
        Analyze emotion trends over a time period
        
        Args:
            duration: Time period in seconds
            
        Returns:
            Dictionary containing trend analysis
        """
        if not self.emotion_history:
            return {'trend': 'insufficient_data'}
        
        current_time = time.time()
        cutoff_time = current_time - duration
        
        # Filter recent emotions
        recent = [
            data for data in self.emotion_history
            if data['timestamp'] >= cutoff_time
        ]
        
        if len(recent) < 2:
            return {'trend': 'insufficient_data'}
        
        # Count emotion occurrences
        emotion_counts = {emotion: 0 for emotion in self.EMOTIONS}
        for data in recent:
            emotion_counts[data['dominant_emotion']] += 1
        
        # Calculate valence and arousal trends
        valences = [data['valence'] for data in recent]
        arousals = [data['arousal'] for data in recent]
        
        # Detect trend direction
        valence_trend = 'stable'
        if len(valences) >= 3:
            if valences[-1] > valences[0] + 0.2:
                valence_trend = 'improving'
            elif valences[-1] < valences[0] - 0.2:
                valence_trend = 'declining'
        
        return {
            'duration': duration,
            'sample_count': len(recent),
            'emotion_distribution': emotion_counts,
            'most_common_emotion': max(emotion_counts.items(), key=lambda x: x[1])[0],
            'avg_valence': float(np.mean(valences)),
            'avg_arousal': float(np.mean(arousals)),
            'valence_trend': valence_trend,
            'valence_std': float(np.std(valences)),
            'arousal_std': float(np.std(arousals))
        }
    
    def detect_emotion_change(self, threshold: float = 0.3) -> Optional[Dict[str, Any]]:
        """
        Detect significant emotion changes
        
        Args:
            threshold: Minimum valence change to consider significant
            
        Returns:
            Change detection data or None if no significant change
        """
        if len(self.emotion_history) < 2:
            return None
        
        current = self.emotion_history[-1]
        previous = self.emotion_history[-2]
        
        valence_change = current['valence'] - previous['valence']
        arousal_change = current['arousal'] - previous['arousal']
        
        if abs(valence_change) >= threshold or abs(arousal_change) >= threshold:
            return {
                'timestamp': current['timestamp'],
                'previous_emotion': previous['dominant_emotion'],
                'current_emotion': current['dominant_emotion'],
                'valence_change': float(valence_change),
                'arousal_change': float(arousal_change),
                'significant': True
            }
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get tracker statistics
        
        Returns:
            Dictionary containing statistics
        """
        success_rate = 0.0
        if self.total_detections + self.failed_detections > 0:
            success_rate = self.total_detections / (
                self.total_detections + self.failed_detections
            )
        
        return {
            'total_detections': self.total_detections,
            'failed_detections': self.failed_detections,
            'success_rate': success_rate,
            'history_size': len(self.emotion_history),
            'deepface_available': DEEPFACE_AVAILABLE
        }
    
    def _get_mock_emotion(self) -> Dict[str, Any]:
        """
        Get mock emotion data when DeepFace is not available
        
        Returns:
            Mock emotion data
        """
        return {
            'timestamp': time.time(),
            'dominant_emotion': 'neutral',
            'confidence': 0.0,
            'all_emotions': {emotion: 0.0 for emotion in self.EMOTIONS},
            'valence': 0.0,
            'arousal': 0.5,
            'mock': True
        }
    
    def reset(self) -> None:
        """Reset tracker state"""
        self.emotion_history.clear()
        self.total_detections = 0
        self.failed_detections = 0
        logger.info("Emotion tracker reset")


# Example usage
if __name__ == "__main__":
    import cv2
    
    print("Starting emotion tracker test...")
    
    try:
        tracker = EmotionTracker(history_size=100, smoothing_window=5)
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("Cannot open camera")
            exit(1)
        
        print("Tracking emotions for 30 seconds...")
        start_time = time.time()
        
        while time.time() - start_time < 30:
            ret, frame = camera.read()
            if not ret:
                continue
            
            # Detect emotion
            emotion_data = tracker.detect_emotion(frame, enforce_detection=False)
            
            if emotion_data:
                print(f"Emotion: {emotion_data['dominant_emotion']}, "
                      f"Confidence: {emotion_data['confidence']:.2f}, "
                      f"Valence: {emotion_data['valence']:.2f}, "
                      f"Arousal: {emotion_data['arousal']:.2f}")
                
                # Check for emotion changes
                change = tracker.detect_emotion_change()
                if change:
                    print(f"  -> Emotion changed from {change['previous_emotion']} "
                          f"to {change['current_emotion']}")
            
            time.sleep(1)
        
        # Print statistics
        stats = tracker.get_statistics()
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Print trend analysis
        trend = tracker.get_emotion_trend(duration=30.0)
        print("\nTrend Analysis:")
        for key, value in trend.items():
            print(f"  {key}: {value}")
        
        camera.release()
        
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
