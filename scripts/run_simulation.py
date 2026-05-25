"""
SubMinds Main Simulation Runner
Integrates facial analysis, TORCS telemetry, and IBM Granite AI
Production-ready with comprehensive error handling
"""
import sys
import time
import logging
import signal
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from facial_analysis.capture import FacialCaptureModule
    from facial_analysis.emotion_tracker import EmotionTracker
    from ai_engine.granite_client import GraniteAIClient
    from utils.logger import setup_logger
    from utils.config_loader import ConfigLoader
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logger = setup_logger('subminds_simulation', 'logs/simulation.log')


class SubMindsSimulation:
    """Main simulation controller for SubMinds system"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SubMinds simulation
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or 'config/camera_config.yaml'
        self.running = False
        
        # Components
        self.facial_capture: Optional[FacialCaptureModule] = None
        self.emotion_tracker: Optional[EmotionTracker] = None
        self.granite_client: Optional[GraniteAIClient] = None
        
        # Statistics
        self.start_time: Optional[float] = None
        self.frames_processed = 0
        self.insights_generated = 0
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("SubMinds simulation initialized")
    
    def initialize_components(self) -> bool:
        """
        Initialize all system components
        
        Returns:
            True if all components initialized successfully
        """
        try:
            logger.info("Initializing components...")
            
            # Initialize facial capture
            logger.info("Initializing facial capture module...")
            self.facial_capture = FacialCaptureModule(
                camera_id=0,
                fps=30,
                buffer_size=1000
            )
            
            # Initialize emotion tracker
            logger.info("Initializing emotion tracker...")
            self.emotion_tracker = EmotionTracker(
                history_size=100,
                smoothing_window=5
            )
            
            # Initialize IBM Granite client
            logger.info("Initializing IBM Granite AI client...")
            self.granite_client = GraniteAIClient(
                config_path='config/ibm_granite_config.yaml'
            )
            
            if not self.granite_client.is_available():
                logger.warning("IBM Granite not available. Running in mock mode.")
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            return False
    
    def start(self, duration: Optional[float] = None) -> None:
        """
        Start the simulation
        
        Args:
            duration: Optional duration in seconds (runs indefinitely if None)
        """
        if not self.initialize_components():
            logger.error("Failed to initialize. Exiting.")
            return
        
        try:
            self.running = True
            self.start_time = time.time()
            
            # Start facial capture
            if not self.facial_capture.start_capture():
                logger.error("Failed to start facial capture")
                return
            
            logger.info("Simulation started. Press Ctrl+C to stop.")
            
            # Main simulation loop
            self._run_simulation_loop(duration)
            
        except Exception as e:
            logger.error(f"Error in simulation: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def _run_simulation_loop(self, duration: Optional[float]) -> None:
        """
        Main simulation loop
        
        Args:
            duration: Optional duration in seconds
        """
        last_analysis_time = time.time()
        analysis_interval = 2.0  # Analyze every 2 seconds
        
        while self.running:
            try:
                # Check duration
                if duration and (time.time() - self.start_time) >= duration:
                    logger.info(f"Simulation duration ({duration}s) reached")
                    break
                
                # Get current frame
                frame_data = self.facial_capture.get_current_frame()
                
                if frame_data:
                    self.frames_processed += 1
                    
                    # Detect emotion
                    emotion_data = self.emotion_tracker.detect_emotion(
                        frame_data['frame'],
                        enforce_detection=False
                    )
                    
                    # Periodic analysis with IBM Granite
                    current_time = time.time()
                    if current_time - last_analysis_time >= analysis_interval:
                        if emotion_data:
                            self._perform_analysis(emotion_data, frame_data)
                        last_analysis_time = current_time
                    
                    # Log progress
                    if self.frames_processed % 30 == 0:  # Every ~1 second at 30fps
                        self._log_progress(emotion_data)
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Error in simulation loop: {e}")
                time.sleep(0.1)
    
    def _perform_analysis(
        self,
        emotion_data: Dict[str, Any],
        frame_data: Dict[str, Any]
    ) -> None:
        """
        Perform AI analysis using IBM Granite
        
        Args:
            emotion_data: Emotion detection results
            frame_data: Frame data with metadata
        """
        try:
            # Mock telemetry data (replace with actual TORCS data)
            telemetry = {
                'speed': 150.0,
                'steering': 0.0,
                'track_position': 0.0,
                'timestamp': frame_data['timestamp']
            }
            
            # Analyze with IBM Granite
            insights = self.granite_client.analyze_subconscious_patterns(
                facial_data=emotion_data,
                telemetry=telemetry
            )
            
            self.insights_generated += 1
            
            # Log insights
            logger.info(f"AI Insights: {insights.get('emotional_state', 'Unknown')}")
            
            # Check for significant changes
            change = self.emotion_tracker.detect_emotion_change()
            if change:
                logger.warning(
                    f"Emotion change detected: {change['previous_emotion']} -> "
                    f"{change['current_emotion']}"
                )
            
        except Exception as e:
            logger.error(f"Error performing analysis: {e}")
    
    def _log_progress(self, emotion_data: Optional[Dict[str, Any]]) -> None:
        """
        Log simulation progress
        
        Args:
            emotion_data: Current emotion data
        """
        elapsed = time.time() - self.start_time
        
        # Get statistics
        capture_stats = self.facial_capture.get_statistics()
        tracker_stats = self.emotion_tracker.get_statistics()
        granite_stats = self.granite_client.get_statistics()
        
        logger.info(
            f"Progress: {elapsed:.1f}s | "
            f"Frames: {self.frames_processed} | "
            f"FPS: {capture_stats['actual_fps']:.1f} | "
            f"Emotion: {emotion_data.get('dominant_emotion', 'N/A') if emotion_data else 'N/A'} | "
            f"Insights: {self.insights_generated}"
        )
    
    def stop(self) -> None:
        """Stop the simulation and cleanup resources"""
        logger.info("Stopping simulation...")
        self.running = False
        
        # Stop facial capture
        if self.facial_capture:
            self.facial_capture.release()
        
        # Print final statistics
        self._print_final_statistics()
        
        logger.info("Simulation stopped")
    
    def _print_final_statistics(self) -> None:
        """Print final simulation statistics"""
        if not self.start_time:
            return
        
        elapsed = time.time() - self.start_time
        
        logger.info("=" * 60)
        logger.info("FINAL STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total Duration: {elapsed:.2f}s")
        logger.info(f"Frames Processed: {self.frames_processed}")
        logger.info(f"Insights Generated: {self.insights_generated}")
        
        if self.facial_capture:
            stats = self.facial_capture.get_statistics()
            logger.info(f"Capture FPS: {stats['actual_fps']:.2f}")
            logger.info(f"Frames Dropped: {stats['frames_dropped']}")
        
        if self.emotion_tracker:
            stats = self.emotion_tracker.get_statistics()
            logger.info(f"Emotion Detection Success Rate: {stats['success_rate']:.2%}")
        
        if self.granite_client:
            stats = self.granite_client.get_statistics()
            logger.info(f"AI Analysis Success Rate: {stats['success_rate']:.2%}")
        
        logger.info("=" * 60)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        logger.info(f"Received signal {signum}. Stopping...")
        self.running = False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SubMinds Simulation Runner')
    parser.add_argument(
        '--duration',
        type=float,
        default=None,
        help='Simulation duration in seconds (default: run indefinitely)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SubMinds - Subconscious Decision Analysis for F1 Drivers")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {'Indefinite' if args.duration is None else f'{args.duration}s'}")
    print("=" * 60)
    print()
    
    # Create and run simulation
    simulation = SubMindsSimulation(config_path=args.config)
    simulation.start(duration=args.duration)
    
    print()
    print("=" * 60)
    print("Simulation Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
