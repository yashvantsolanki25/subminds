"""
Real-time emotion tracking and history management
"""
from typing import Dict, Any, List, Optional
from collections import deque
from datetime import datetime
import numpy as np

from ..utils.logger import get_logger

logger = get_logger(__name__)


class EmotionTracker:
    """Track emotions over time and detect patterns"""
    
    def __init__(self, history_size: int = 1000):
        """
        Initialize emotion tracker
        
        Args:
            history_size: Maximum number of emotion records to keep
        """
        self.history_size = history_size
        self.emotion_history = deque(maxlen=history_size)
        self.stress_history = deque(maxlen=history_size)
        
        logger.info(f"EmotionTracker initialized with history size: {history_size}")
        
    def add_emotion(
        self,
        emotion_data: Dict[str, Any],
        timestamp: Optional[float] = None
    ):
        """
        Add emotion data to history
        
        Args:
            emotion_data: Emotion detection results
            timestamp: Optional timestamp (uses current time if not provided)
        """
        if timestamp is None:
            timestamp = datetime.now().timestamp()
            
        record = {
            'timestamp': timestamp,
            'dominant_emotion': emotion_data.get('dominant_emotion', 'neutral'),
            'confidence': emotion_data.get('confidence', 0.0),
            'valence': emotion_data.get('valence', 0.0),
            'arousal': emotion_data.get('arousal', 0.0),
            'emotions': emotion_data.get('emotions', {})
        }
        
        self.emotion_history.append(record)
        
        # Calculate and store stress level
        stress_level = self._calculate_stress(emotion_data.get('emotions', {}))
        self.stress_history.append({
            'timestamp': timestamp,
            'stress_level': stress_level
        })
        
    def get_current_emotion(self) -> Optional[Dict[str, Any]]:
        """Get the most recent emotion record"""
        return self.emotion_history[-1] if self.emotion_history else None
        
    def get_emotion_history(self, n: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent emotion history
        
        Args:
            n: Number of records to retrieve
            
        Returns:
            List of emotion records
        """
        return list(self.emotion_history)[-n:]
        
    def get_dominant_emotion_over_time(
        self,
        time_window: float = 60.0
    ) -> Optional[str]:
        """
        Get the dominant emotion over a time window
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Most frequent emotion in the time window
        """
        if not self.emotion_history:
            return None
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        # Filter records within time window
        recent_emotions = [
            record['dominant_emotion']
            for record in self.emotion_history
            if record['timestamp'] >= cutoff_time
        ]
        
        if not recent_emotions:
            return None
            
        # Find most common emotion
        from collections import Counter
        emotion_counts = Counter(recent_emotions)
        return emotion_counts.most_common(1)[0][0]
        
    def get_average_valence(self, time_window: float = 60.0) -> float:
        """
        Calculate average valence over time window
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Average valence score
        """
        if not self.emotion_history:
            return 0.0
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        valences = [
            record['valence']
            for record in self.emotion_history
            if record['timestamp'] >= cutoff_time
        ]
        
        return np.mean(valences) if valences else 0.0
        
    def get_average_arousal(self, time_window: float = 60.0) -> float:
        """
        Calculate average arousal over time window
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Average arousal score
        """
        if not self.emotion_history:
            return 0.5
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        arousals = [
            record['arousal']
            for record in self.emotion_history
            if record['timestamp'] >= cutoff_time
        ]
        
        return np.mean(arousals) if arousals else 0.5
        
    def get_stress_level(self, time_window: float = 60.0) -> float:
        """
        Calculate average stress level over time window
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Average stress level (0-10)
        """
        if not self.stress_history:
            return 0.0
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        stress_levels = [
            record['stress_level']
            for record in self.stress_history
            if record['timestamp'] >= cutoff_time
        ]
        
        return np.mean(stress_levels) if stress_levels else 0.0
        
    def detect_emotion_change(
        self,
        threshold: float = 0.5,
        time_window: float = 10.0
    ) -> Optional[Dict[str, Any]]:
        """
        Detect significant emotion changes
        
        Args:
            threshold: Minimum valence change to detect
            time_window: Time window to check for changes
            
        Returns:
            Change detection result or None
        """
        if len(self.emotion_history) < 2:
            return None
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        # Get recent records
        recent = [
            record for record in self.emotion_history
            if record['timestamp'] >= cutoff_time
        ]
        
        if len(recent) < 2:
            return None
            
        # Compare first and last
        first = recent[0]
        last = recent[-1]
        
        valence_change = abs(last['valence'] - first['valence'])
        
        if valence_change >= threshold:
            return {
                'detected': True,
                'from_emotion': first['dominant_emotion'],
                'to_emotion': last['dominant_emotion'],
                'valence_change': last['valence'] - first['valence'],
                'time_span': last['timestamp'] - first['timestamp']
            }
            
        return None
        
    def detect_stress_spike(
        self,
        threshold: float = 3.0,
        time_window: float = 10.0
    ) -> bool:
        """
        Detect sudden stress increase
        
        Args:
            threshold: Minimum stress increase to detect
            time_window: Time window to check
            
        Returns:
            True if stress spike detected
        """
        if len(self.stress_history) < 2:
            return False
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        recent = [
            record for record in self.stress_history
            if record['timestamp'] >= cutoff_time
        ]
        
        if len(recent) < 2:
            return False
            
        stress_increase = recent[-1]['stress_level'] - recent[0]['stress_level']
        
        return stress_increase >= threshold
        
    def get_emotion_statistics(
        self,
        time_window: float = 300.0
    ) -> Dict[str, Any]:
        """
        Get comprehensive emotion statistics
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Dictionary with emotion statistics
        """
        if not self.emotion_history:
            return {
                'dominant_emotion': 'neutral',
                'average_valence': 0.0,
                'average_arousal': 0.5,
                'average_stress': 0.0,
                'emotion_distribution': {},
                'sample_count': 0
            }
            
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - time_window
        
        recent = [
            record for record in self.emotion_history
            if record['timestamp'] >= cutoff_time
        ]
        
        if not recent:
            return self.get_emotion_statistics(time_window * 2)
            
        # Calculate statistics
        from collections import Counter
        emotions = [r['dominant_emotion'] for r in recent]
        emotion_counts = Counter(emotions)
        
        return {
            'dominant_emotion': emotion_counts.most_common(1)[0][0],
            'average_valence': np.mean([r['valence'] for r in recent]),
            'average_arousal': np.mean([r['arousal'] for r in recent]),
            'average_stress': self.get_stress_level(time_window),
            'emotion_distribution': dict(emotion_counts),
            'sample_count': len(recent),
            'time_window': time_window
        }
        
    def _calculate_stress(self, emotions: Dict[str, float]) -> float:
        """Calculate stress level from emotions"""
        stress_weights = {
            'angry': 1.0,
            'fear': 1.0,
            'disgust': 0.7,
            'sad': 0.5,
            'surprise': 0.3
        }
        
        stress = sum(
            emotions.get(emotion, 0) * weight
            for emotion, weight in stress_weights.items()
        )
        
        return min(stress / 10.0, 1.0) * 10
        
    def clear_history(self):
        """Clear all emotion history"""
        self.emotion_history.clear()
        self.stress_history.clear()
        logger.info("Emotion history cleared")
        
    def export_history(self) -> List[Dict[str, Any]]:
        """Export emotion history for analysis"""
        return list(self.emotion_history)


# Example usage
if __name__ == "__main__":
    from ..utils.logger import setup_logger
    import time
    
    setup_logger(__name__, level="DEBUG")
    
    tracker = EmotionTracker(history_size=1000)
    
    # Simulate emotion tracking
    emotions = ['happy', 'neutral', 'focused', 'stressed', 'calm']
    
    for i in range(10):
        emotion_data = {
            'dominant_emotion': emotions[i % len(emotions)],
            'confidence': 0.8,
            'valence': np.random.uniform(-0.5, 0.5),
            'arousal': np.random.uniform(0.3, 0.7),
            'emotions': {
                'happy': np.random.uniform(0, 100),
                'sad': np.random.uniform(0, 100),
                'angry': np.random.uniform(0, 100),
                'neutral': np.random.uniform(0, 100)
            }
        }
        
        tracker.add_emotion(emotion_data)
        time.sleep(0.5)
        
    # Get statistics
    stats = tracker.get_emotion_statistics(time_window=10.0)
    logger.info(f"Emotion statistics: {stats}")
    
    # Check for stress spike
    if tracker.detect_stress_spike():
        logger.warning("Stress spike detected!")

# Made with Bob
