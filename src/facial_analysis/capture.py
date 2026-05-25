"""
Webcam capture module for facial expression analysis
"""
import cv2
import mediapipe as mp
import time
import threading
from collections import deque
from typing import Optional, Dict, Any, List
import numpy as np
from pathlib import Path

from ..utils.logger import get_logger

logger = get_logger(__name__)


class FacialCaptureModule:
    """Captures and processes facial expressions from webcam"""
    
    def __init__(
        self,
        camera_id: int = 0,
        fps: int = 30,
        buffer_size: int = 1000,
        save_video: bool = False,
        output_dir: str = "data/raw/video"
    ):
        """
        Initialize facial capture module
        
        Args:
            camera_id: Camera device ID
            fps: Target frames per second
            buffer_size: Maximum buffer size for frames
            save_video: Whether to save video to disk
            output_dir: Directory to save videos
        """
        self.camera_id = camera_id
        self.fps = fps
        self.buffer_size = buffer_size
        self.save_video = save_video
        self.output_dir = Path(output_dir)
        
        # Create output directory
        if self.save_video:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize camera
        logger.info(f"Initializing camera {camera_id}")
        self.camera = cv2.VideoCapture(camera_id)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        if not self.camera.isOpened():
            raise RuntimeError(f"Failed to open camera {camera_id}")
        
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
            min_tracking_confidence=0.5,
            refine_landmarks=True
        )
        
        # Buffer for captured frames
        self.buffer = deque(maxlen=buffer_size)
        
        # Threading
        self.is_capturing = False
        self.capture_thread = None
        
        # Video writer
        self.video_writer = None
        if self.save_video:
            self._init_video_writer()
        
        logger.info("Facial capture module initialized successfully")
        
    def _init_video_writer(self):
        """Initialize video writer for saving recordings"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        video_path = self.output_dir / f"session_{timestamp}.mp4"
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            str(video_path),
            fourcc,
            self.fps,
            (1280, 720)
        )
        logger.info(f"Video writer initialized: {video_path}")
        
    def start_capture(self):
        """Start capturing frames in a separate thread"""
        if not self.is_capturing:
            logger.info("Starting facial capture")
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
        else:
            logger.warning("Capture already running")
            
    def stop_capture(self):
        """Stop capturing frames"""
        if self.is_capturing:
            logger.info("Stopping facial capture")
            self.is_capturing = False
            if self.capture_thread:
                self.capture_thread.join(timeout=5.0)
        
    def _capture_loop(self):
        """Main capture loop (runs in separate thread)"""
        frame_count = 0
        start_time = time.time()
        
        while self.is_capturing:
            ret, frame = self.camera.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                break
                
            timestamp = time.time()
            
            # Detect faces
            faces = self._detect_faces(frame)
            
            # Get facial landmarks
            landmarks = self._get_landmarks(frame) if faces else None
            
            # Store in buffer
            frame_data = {
                'timestamp': timestamp,
                'frame': frame.copy(),
                'faces': faces,
                'landmarks': landmarks,
                'frame_number': frame_count
            }
            self.buffer.append(frame_data)
            
            # Save to video if enabled
            if self.video_writer:
                self.video_writer.write(frame)
            
            frame_count += 1
            
            # Log FPS every 100 frames
            if frame_count % 100 == 0:
                elapsed = time.time() - start_time
                actual_fps = frame_count / elapsed
                logger.debug(f"Captured {frame_count} frames, FPS: {actual_fps:.2f}")
            
            # Control frame rate
            time.sleep(1.0 / self.fps)
            
        logger.info(f"Capture loop ended. Total frames: {frame_count}")
            
    def _detect_faces(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect faces in frame using MediaPipe
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected faces with bounding boxes
        """
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
        
    def _get_landmarks(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Extract facial landmarks using MediaPipe Face Mesh
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary containing facial landmarks or None
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            return {
                'landmarks': [
                    {'x': lm.x, 'y': lm.y, 'z': lm.z}
                    for lm in landmarks.landmark
                ],
                'num_landmarks': len(landmarks.landmark)
            }
        return None
        
    def get_current_frame(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent captured frame
        
        Returns:
            Dictionary containing frame data or None
        """
        return self.buffer[-1] if self.buffer else None
        
    def get_frame_history(self, n: int = 100) -> List[Dict[str, Any]]:
        """
        Get last n frames from buffer
        
        Args:
            n: Number of frames to retrieve
            
        Returns:
            List of frame data dictionaries
        """
        return list(self.buffer)[-n:]
        
    def get_buffer_size(self) -> int:
        """Get current buffer size"""
        return len(self.buffer)
        
    def clear_buffer(self):
        """Clear the frame buffer"""
        self.buffer.clear()
        logger.info("Frame buffer cleared")
        
    def release(self):
        """Release camera and cleanup resources"""
        logger.info("Releasing facial capture resources")
        self.stop_capture()
        
        if self.camera:
            self.camera.release()
            
        if self.video_writer:
            self.video_writer.release()
            
        if self.face_detection:
            self.face_detection.close()
            
        if self.face_mesh:
            self.face_mesh.close()
            
        logger.info("Resources released successfully")
        
    def __enter__(self):
        """Context manager entry"""
        self.start_capture()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()


# Example usage
if __name__ == "__main__":
    import sys
    
    # Setup logging
    from ..utils.logger import setup_logger
    setup_logger(__name__, level="DEBUG")
    
    logger.info("Starting facial capture test")
    
    try:
        with FacialCaptureModule(camera_id=0, fps=30, save_video=True) as capture:
            logger.info("Capture started. Press Ctrl+C to stop...")
            
            while True:
                frame_data = capture.get_current_frame()
                if frame_data:
                    faces_count = len(frame_data['faces'])
                    has_landmarks = frame_data['landmarks'] is not None
                    logger.info(
                        f"Frame {frame_data['frame_number']}: "
                        f"{faces_count} faces, "
                        f"landmarks: {has_landmarks}"
                    )
                time.sleep(1)
                
    except KeyboardInterrupt:
        logger.info("Stopping capture...")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

# Made with Bob
