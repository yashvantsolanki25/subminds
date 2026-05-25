"""
Facial analysis module for SubMinds
"""
from .capture import FacialCaptureModule
from .expression_detector import ExpressionDetector
from .emotion_tracker import EmotionTracker

__all__ = [
    'FacialCaptureModule',
    'ExpressionDetector',
    'EmotionTracker'
]

# Made with Bob
