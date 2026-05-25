"""
Webcam capture module for facial expression analysis
Production-ready implementation with comprehensive error handling
"""
import cv2
import time
import threading
import logging
from collections import deque
from typing import Optional, Dict, Any, List
import numpy as np
from pathlib import Path

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logging.warning("MediaPipe not available. Install with: pip install mediapipe")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacialCaptureModule:
    """Captures and processes facial expressions from webcam"""
    
    def __init__(
        self, 
        camera_id: int = 0, 
        fps: int = 30, 
        buffer_size: int = 1000,
        width: int = 1280,
        height: int = 720
    ):
        """
        Initialize facial capture module
        
        Args:
            camera_id: Camera device ID
            fps: Target frames per second
            buffer_size: Maximum buffer size for frames
            width: Camera width resolution
            height: Camera height resolution
        """
        self.camera_id = camera_id
        self.fps = fps
        self.buffer_size = buffer_size
        self.width = width
        self.height = height
        
        # Initialize camera with error handling
        try:
            self.camera = cv2.VideoCapture(camera_id)
            if not self.camera.isOpened():
                raise RuntimeError(f"Cannot open camera {camera_id}")
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            logger.info(f"Camera {camera_id} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            raise
        
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = None
        self.face_detection = None
        self.mp_face_mesh = None
        self.face_mesh = None
        
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face_detection = mp.solutions.face_detection
                self.face_detection = self.mp_face_detection.FaceDetection(
                    min_detection_confidence=0.7,
                    model_selection=0
                )
                logger.info("MediaPipe Face Detection initialized")
            except Exception as e:
                logger.error(f"Failed to initialize face detection: {e}")
                self.face_detection = None
            
            # Initialize MediaPipe Face Mesh
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.5
                )
                logger.info("MediaPipe Face Mesh initialized")
            except Exception as e:
                logger.error(f"Failed to initialize face mesh: {e}")
                self.face_mesh = None
        else:
            logger.warning("MediaPipe not available. Face detection disabled.")
        
        # Buffer for captured frames
        self.buffer = deque(maxlen=buffer_size)
        
        # Threading
        self.is_capturing = False
        self.capture_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Statistics
        self.frames_captured = 0
        self.frames_dropped = 0
        self.start_time = None
        
    def start_capture(self) -> bool:
        """
        Start capturing frames in a separate thread
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_capturing:
            logger.warning("Capture already running")
            return False
        
        try:
            self.is_capturing = True
            self.start_time = time.time()
            self.capture_thread = threading.Thread(
                target=self._capture_loop,
                daemon=True
            )
            self.capture_thread.start()
            logger.info("Capture thread started")
            return True
        except Exception as e:
            logger.error(f"Failed to start capture: {e}")
            self.is_capturing = False
            return False
            
    def stop_capture(self) -> None:
        """Stop capturing frames"""
        if not self.is_capturing:
            logger.warning("Capture not running")
            return
        
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5.0)
            if self.capture_thread.is_alive():
                logger.warning("Capture thread did not stop gracefully")
        
        logger.info(f"Capture stopped. Frames captured: {self.frames_captured}, "
                   f"Frames dropped: {self.frames_dropped}")
            
    def _capture_loop(self) -> None:
        """Main capture loop (runs in separate thread)"""
        frame_interval = 1.0 / self.fps
        last_frame_time = time.time()
        
        while self.is_capturing:
            try:
                current_time = time.time()
                
                # Control frame rate
                if current_time - last_frame_time < frame_interval:
                    time.sleep(0.001)  # Small sleep to prevent CPU spinning
                    continue
                
                ret, frame = self.camera.read()
                if not ret:
                    logger.warning("Failed to read frame from camera")
                    self.frames_dropped += 1
                    continue
                
                timestamp = current_time
                last_frame_time = current_time
                
                # Detect faces
                faces = self._detect_faces(frame)
                
                # Get facial landmarks if faces detected
                landmarks = None
                if faces:
                    landmarks = self._get_landmarks(frame)
                
                # Store in buffer with thread safety
                frame_data = {
                    'timestamp': timestamp,
                    'frame': frame.copy(),
                    'faces': faces,
                    'landmarks': landmarks,
                    'frame_number': self.frames_captured
                }
                
                with self._lock:
                    self.buffer.append(frame_data)
                
                self.frames_captured += 1
                
            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                self.frames_dropped += 1
                time.sleep(0.1)  # Brief pause on error
                
    def _detect_faces(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect faces in frame using MediaPipe
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected faces with bounding boxes
        """
        if not self.face_detection:
            return []
            
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_frame)
            
            faces = []
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    faces.append({
                        'bbox': {
                            'x': float(bbox.xmin),
                            'y': float(bbox.ymin),
                            'width': float(bbox.width),
                            'height': float(bbox.height)
                        },
                        'confidence': float(detection.score[0])
                    })
            return faces
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
        
    def _get_landmarks(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Extract facial landmarks using MediaPipe Face Mesh
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary containing landmarks or None if no face detected
        """
        if not self.face_mesh:
            return None
            
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                return {
                    'landmarks': [
                        {
                            'x': float(lm.x),
                            'y': float(lm.y),
                            'z': float(lm.z)
                        }
                        for lm in landmarks.landmark
                    ],
                    'num_landmarks': len(landmarks.landmark)
                }
            return None
        except Exception as e:
            logger.error(f"Error extracting landmarks: {e}")
            return None
        
    def get_current_frame(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent captured frame
        
        Returns:
            Most recent frame data or None if buffer is empty
        """
        with self._lock:
            return self.buffer[-1] if self.buffer else None
        
    def get_frame_history(self, n: int = 100) -> List[Dict[str, Any]]:
        """
        Get last n frames from buffer
        
        Args:
            n: Number of frames to retrieve
            
        Returns:
            List of frame data dictionaries
        """
        with self._lock:
            return list(self.buffer)[-n:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get capture statistics
        
        Returns:
            Dictionary containing capture statistics
        """
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        actual_fps = self.frames_captured / elapsed_time if elapsed_time > 0 else 0
        
        return {
            'frames_captured': self.frames_captured,
            'frames_dropped': self.frames_dropped,
            'buffer_size': len(self.buffer),
            'elapsed_time': elapsed_time,
            'actual_fps': actual_fps,
            'target_fps': self.fps,
            'is_capturing': self.is_capturing
        }
    
    def save_frame(self, frame_data: Dict[str, Any], output_path: str) -> bool:
        """
        Save a frame to disk
        
        Args:
            frame_data: Frame data dictionary
            output_path: Path to save the frame
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            path_obj = Path(output_path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            success = cv2.imwrite(str(path_obj), frame_data['frame'])
            if success:
                logger.info(f"Frame saved to {output_path}")
            else:
                logger.error(f"Failed to save frame to {output_path}")
            return success
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return False
        
    def release(self) -> None:
        """Release camera resources"""
        try:
            self.stop_capture()
            
            if self.camera:
                self.camera.release()
                logger.info("Camera released")
            
            if self.face_detection:
                self.face_detection.close()
            
            if self.face_mesh:
                self.face_mesh.close()
                
            logger.info("All resources released")
        except Exception as e:
            logger.error(f"Error releasing resources: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()


# Example usage
if __name__ == "__main__":
    print("Starting facial capture test...")
    
    try:
        # Use context manager for automatic cleanup
        with FacialCaptureModule(camera_id=0, fps=30) as capture:
            # Start capture
            if not capture.start_capture():
                print("Failed to start capture")
                exit(1)
            
            print("Capturing for 10 seconds...")
            start_time = time.time()
            
            # Capture for 10 seconds
            while time.time() - start_time < 10:
                frame_data = capture.get_current_frame()
                if frame_data:
                    stats = capture.get_statistics()
                    print(f"Frame {frame_data['frame_number']}: "
                          f"Faces detected: {len(frame_data['faces'])}, "
                          f"FPS: {stats['actual_fps']:.2f}")
                time.sleep(1)
            
            # Print final statistics
            final_stats = capture.get_statistics()
            print("\nFinal Statistics:")
            for key, value in final_stats.items():
                print(f"  {key}: {value}")
                
    except KeyboardInterrupt:
        print("\nStopping capture...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
