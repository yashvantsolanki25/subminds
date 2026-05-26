"""
Facial Capture Module
Captures video from webcam for facial analysis
"""
import cv2
import logging
from typing import Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class FacialCapture:
    """Captures facial expressions from webcam"""
    
    def __init__(self, camera_id: int = 0):
        """
        Initialize facial capture
        
        Args:
            camera_id: Camera device ID (0 for default)
        """
        self.camera_id = camera_id
        self.capture: Optional[cv2.VideoCapture] = None
        self.is_capturing = False
        
        try:
            self.capture = cv2.VideoCapture(camera_id)
            if self.capture.isOpened():
                logger.info(f"Camera {camera_id} opened successfully")
            else:
                logger.warning(f"Could not open camera {camera_id}")
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
    
    def start_capture(self) -> bool:
        """
        Start capturing video
        
        Returns:
            True if capture started successfully
        """
        if self.capture and self.capture.isOpened():
            self.is_capturing = True
            logger.info("Capture started")
            return True
        return False
    
    def stop_capture(self):
        """Stop capturing video"""
        self.is_capturing = False
        logger.info("Capture stopped")
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Get current frame from camera
        
        Returns:
            Frame as numpy array or None if failed
        """
        if not self.capture or not self.is_capturing:
            return None
        
        ret, frame = self.capture.read()
        if ret:
            return frame
        return None
    
    def release(self):
        """Release camera resources"""
        if self.capture:
            self.capture.release()
            logger.info("Camera released")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()


# Made with Bob
