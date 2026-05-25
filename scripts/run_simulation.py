#!/usr/bin/env python3
"""
Main script to run SubMinds simulation
"""
import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.logger import setup_logger
from utils.config_loader import get_config_loader
from facial_analysis import FacialCaptureModule, ExpressionDetector, EmotionTracker
from ai_engine import GraniteAIClient, PatternRecognitionEngine

logger = setup_logger(__name__, log_file='logs/simulation.log', level='INFO')


def main():
    """Main simulation loop"""
    logger.info("=" * 60)
    logger.info("SubMinds - Subconscious Decision Analysis")
    logger.info("=" * 60)
    
    try:
        # Load configurations
        logger.info("Loading configurations...")
        config_loader = get_config_loader()
        camera_config = config_loader.load_yaml('camera_config.yaml')
        
        # Initialize components
        logger.info("Initializing components...")
        
        # Facial analysis
        facial_capture = FacialCaptureModule(
            camera_id=camera_config['camera']['device']['id'],
            fps=camera_config['camera']['device']['fps'],
            save_video=camera_config['camera']['recording']['enabled']
        )
        
        expression_detector = ExpressionDetector()
        emotion_tracker = EmotionTracker(history_size=1000)
        
        # AI Engine
        granite_client = GraniteAIClient()
        pattern_engine = PatternRecognitionEngine()
        
        logger.info("All components initialized successfully")
        
        # Start facial capture
        logger.info("Starting facial capture...")
        facial_capture.start_capture()
        
        # Wait for initial frames
        time.sleep(2)
        
        logger.info("Simulation running. Press Ctrl+C to stop...")
        logger.info("-" * 60)
        
        frame_count = 0
        analysis_interval = 30  # Analyze every 30 frames
        
        while True:
            # Get current frame
            frame_data = facial_capture.get_current_frame()
            
            if frame_data and frame_data['faces']:
                frame_count += 1
                
                # Detect expression
                expression = expression_detector.detect_emotion(frame_data['frame'])
                
                # Track emotion
                emotion_tracker.add_emotion(expression, frame_data['timestamp'])
                
                # Log current state
                if frame_count % 30 == 0:  # Log every 30 frames
                    logger.info(
                        f"Frame {frame_count}: "
                        f"Emotion={expression['dominant_emotion']} "
                        f"({expression['confidence']:.2f}), "
                        f"Stress={emotion_tracker.get_stress_level(60.0):.1f}/10, "
                        f"Valence={expression['valence']:.2f}"
                    )
                
                # Perform AI analysis periodically
                if frame_count % analysis_interval == 0:
                    logger.info("Performing AI analysis...")
                    
                    # Get emotion statistics
                    emotion_stats = emotion_tracker.get_emotion_statistics(60.0)
                    
                    # Simulate telemetry (in real scenario, get from TORCS)
                    telemetry = {
                        'speed': 150.0,
                        'steering': 0.0,
                        'track_position': 0.0,
                        'lap_time': 95.0
                    }
                    
                    # Analyze with IBM Granite
                    insights = granite_client.analyze_subconscious_patterns(
                        facial_data={
                            'dominant_emotion': emotion_stats['dominant_emotion'],
                            'stress_level': emotion_stats['average_stress'],
                            'valence': emotion_stats['average_valence'],
                            'arousal': emotion_stats['average_arousal'],
                            'confidence': 0.85
                        },
                        telemetry=telemetry
                    )
                    
                    logger.info(f"AI Insights: {insights.get('analysis_complete', False)}")
                    
                    # Detect patterns
                    emotion_history = emotion_tracker.get_emotion_history(100)
                    stress_pattern = pattern_engine.detect_stress_pattern(
                        emotion_history,
                        []  # Empty telemetry for now
                    )
                    
                    if stress_pattern.get('detected'):
                        logger.warning(
                            f"Stress pattern detected: "
                            f"{len(stress_pattern.get('patterns', []))} patterns"
                        )
            
            # Control loop rate
            time.sleep(0.033)  # ~30 FPS
            
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        
    except Exception as e:
        logger.error(f"Error in simulation: {e}", exc_info=True)
        return 1
        
    finally:
        # Cleanup
        logger.info("Cleaning up resources...")
        if 'facial_capture' in locals():
            facial_capture.release()
        logger.info("Simulation ended")
        
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
