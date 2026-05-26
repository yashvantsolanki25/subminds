"""
Facial analysis module for SubMinds
"""
from .capture import FacialCapture
from .expression_detector import ExpressionDetector
from .emotion_tracker import EmotionTracker

__all__ = [
    'FacialCapture',
    'ExpressionDetector',
    'EmotionTracker'
]

# Made with Bob
