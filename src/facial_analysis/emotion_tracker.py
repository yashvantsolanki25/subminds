"""
Emotion Tracker Module
Tracks emotional states over time
"""
import logging
from typing import Dict, Any, List
from collections import deque
import time

logger = logging.getLogger(__name__)


class EmotionTracker:
    """Tracks emotional states and patterns over time"""
    
    def __init__(self, history_size: int = 100):
        """
        Initialize emotion tracker
        
        Args:
            history_size: Number of emotion records to keep in history
        """
        self.history_size = history_size
        self.emotion_history: deque = deque(maxlen=history_size)
        self.start_time = time.time()
        
        logger.info("Emotion tracker initialized")
    
    def add_emotion(self, emotion_data: Dict[str, Any]):
        """
        Add emotion data to history
        
        Args:
            emotion_data: Dictionary containing emotion information
        """
        timestamp = time.time()
        record = {
            'timestamp': timestamp,
            'elapsed': timestamp - self.start_time,
            **emotion_data
        }
        self.emotion_history.append(record)
    
    def get_current_emotion(self) -> Dict[str, Any]:
        """
        Get most recent emotion data
        
        Returns:
            Most recent emotion record or empty dict
        """
        if self.emotion_history:
            return self.emotion_history[-1]
        return {}
    
    def get_history(self, count: int = None) -> List[Dict[str, Any]]:
        """
        Get emotion history
        
        Args:
            count: Number of recent records to return (None for all)
            
        Returns:
            List of emotion records
        """
        if count is None:
            return list(self.emotion_history)
        return list(self.emotion_history)[-count:]
    
    def get_dominant_emotion(self, window: int = 10) -> str:
        """
        Get dominant emotion over recent window
        
        Args:
            window: Number of recent records to analyze
            
        Returns:
            Most common emotion in window
        """
        recent = self.get_history(window)
        if not recent:
            return "neutral"
        
        emotions = [r.get('dominant_emotion', 'neutral') for r in recent]
        return max(set(emotions), key=emotions.count)
    
    def get_average_valence(self, window: int = 10) -> float:
        """
        Get average emotional valence over window
        
        Args:
            window: Number of recent records to analyze
            
        Returns:
            Average valence (-1 to 1)
        """
        recent = self.get_history(window)
        if not recent:
            return 0.0
        
        valences = [r.get('valence', 0.0) for r in recent]
        return sum(valences) / len(valences)
    
    def get_stress_trend(self, window: int = 10) -> str:
        """
        Get stress level trend
        
        Args:
            window: Number of recent records to analyze
            
        Returns:
            Trend description: "increasing", "decreasing", or "stable"
        """
        recent = self.get_history(window)
        if len(recent) < 2:
            return "stable"
        
        stress_levels = [r.get('stress_level', 5) for r in recent]
        
        # Simple trend analysis
        first_half = sum(stress_levels[:len(stress_levels)//2])
        second_half = sum(stress_levels[len(stress_levels)//2:])
        
        if second_half > first_half * 1.1:
            return "increasing"
        elif second_half < first_half * 0.9:
            return "decreasing"
        return "stable"
    
    def reset(self):
        """Reset emotion history"""
        self.emotion_history.clear()
        self.start_time = time.time()
        logger.info("Emotion history reset")


# Made with Bob
