"""
Pattern recognition engine for identifying subconscious patterns
"""
from typing import Dict, Any, List, Optional
from collections import defaultdict
import numpy as np

from ..utils.logger import get_logger

logger = get_logger(__name__)


class PatternRecognitionEngine:
    """Detect and analyze patterns in driver behavior"""
    
    def __init__(self):
        """Initialize pattern recognition engine"""
        self.patterns = defaultdict(list)
        self.pattern_confidence = {}
        logger.info("Pattern Recognition Engine initialized")
        
    def detect_stress_pattern(
        self,
        emotion_history: List[Dict[str, Any]],
        telemetry_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect stress patterns from emotion and telemetry data
        
        Args:
            emotion_history: List of emotion records
            telemetry_history: List of telemetry records
            
        Returns:
            Detected stress patterns
        """
        if len(emotion_history) < 10:
            return {'detected': False, 'reason': 'Insufficient data'}
            
        try:
            # Extract stress levels
            stress_levels = [
                record.get('stress_level', 0)
                for record in emotion_history
            ]
            
            # Calculate statistics
            avg_stress = np.mean(stress_levels)
            max_stress = np.max(stress_levels)
            stress_variance = np.var(stress_levels)
            
            # Detect patterns
            patterns = []
            
            # High baseline stress
            if avg_stress > 6.0:
                patterns.append({
                    'type': 'high_baseline_stress',
                    'severity': 'high',
                    'description': 'Consistently elevated stress levels',
                    'avg_stress': avg_stress
                })
                
            # Stress spikes
            stress_spikes = self._detect_spikes(stress_levels, threshold=3.0)
            if stress_spikes:
                patterns.append({
                    'type': 'stress_spikes',
                    'severity': 'medium',
                    'description': f'{len(stress_spikes)} stress spikes detected',
                    'spike_count': len(stress_spikes),
                    'spike_indices': stress_spikes
                })
                
            # High variability
            if stress_variance > 4.0:
                patterns.append({
                    'type': 'high_stress_variability',
                    'severity': 'medium',
                    'description': 'Unstable stress levels',
                    'variance': stress_variance
                })
                
            return {
                'detected': len(patterns) > 0,
                'patterns': patterns,
                'statistics': {
                    'avg_stress': avg_stress,
                    'max_stress': max_stress,
                    'variance': stress_variance
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting stress pattern: {e}")
            return {'detected': False, 'error': str(e)}
            
    def detect_emotion_performance_correlation(
        self,
        emotion_history: List[Dict[str, Any]],
        performance_metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect correlations between emotions and performance
        
        Args:
            emotion_history: List of emotion records
            performance_metrics: List of performance records
            
        Returns:
            Correlation analysis results
        """
        if len(emotion_history) < 10 or len(performance_metrics) < 10:
            return {'detected': False, 'reason': 'Insufficient data'}
            
        try:
            # Align data by timestamp
            aligned_data = self._align_data(emotion_history, performance_metrics)
            
            if len(aligned_data) < 5:
                return {'detected': False, 'reason': 'Insufficient aligned data'}
                
            # Extract features
            valences = [d['emotion']['valence'] for d in aligned_data]
            arousals = [d['emotion']['arousal'] for d in aligned_data]
            lap_times = [d['performance'].get('lap_time', 0) for d in aligned_data]
            
            # Calculate correlations
            valence_performance_corr = np.corrcoef(valences, lap_times)[0, 1]
            arousal_performance_corr = np.corrcoef(arousals, lap_times)[0, 1]
            
            # Identify optimal states
            optimal_valence = self._find_optimal_range(valences, lap_times)
            optimal_arousal = self._find_optimal_range(arousals, lap_times)
            
            return {
                'detected': True,
                'correlations': {
                    'valence_performance': valence_performance_corr,
                    'arousal_performance': arousal_performance_corr
                },
                'optimal_states': {
                    'valence': optimal_valence,
                    'arousal': optimal_arousal
                },
                'sample_size': len(aligned_data)
            }
            
        except Exception as e:
            logger.error(f"Error detecting correlation: {e}")
            return {'detected': False, 'error': str(e)}
            
    def detect_decision_pattern(
        self,
        action_history: List[Dict[str, Any]],
        emotion_context: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect decision-making patterns
        
        Args:
            action_history: List of driver actions
            emotion_context: Corresponding emotion states
            
        Returns:
            Decision pattern analysis
        """
        if len(action_history) < 10:
            return {'detected': False, 'reason': 'Insufficient data'}
            
        try:
            patterns = []
            
            # Analyze aggressive vs conservative decisions
            aggressive_count = sum(
                1 for action in action_history
                if abs(action.get('steering', 0)) > 0.5
            )
            
            if aggressive_count / len(action_history) > 0.3:
                patterns.append({
                    'type': 'aggressive_driving',
                    'frequency': aggressive_count / len(action_history),
                    'description': 'Tendency toward aggressive maneuvers'
                })
                
            # Analyze hesitation patterns
            hesitation_count = sum(
                1 for action in action_history
                if abs(action.get('steering', 0)) < 0.1 and
                   action.get('speed', 0) < 100
            )
            
            if hesitation_count / len(action_history) > 0.2:
                patterns.append({
                    'type': 'hesitation',
                    'frequency': hesitation_count / len(action_history),
                    'description': 'Hesitation in decision-making'
                })
                
            return {
                'detected': len(patterns) > 0,
                'patterns': patterns,
                'total_actions': len(action_history)
            }
            
        except Exception as e:
            logger.error(f"Error detecting decision pattern: {e}")
            return {'detected': False, 'error': str(e)}
            
    def detect_micro_expression_pattern(
        self,
        micro_expressions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect patterns in micro-expressions
        
        Args:
            micro_expressions: List of detected micro-expressions
            
        Returns:
            Micro-expression pattern analysis
        """
        if len(micro_expressions) < 5:
            return {'detected': False, 'reason': 'Insufficient micro-expressions'}
            
        try:
            # Group by emotion transitions
            transitions = defaultdict(int)
            for me in micro_expressions:
                from_emotion = me.get('from_emotion')
                to_emotion = me.get('to_emotion')
                if from_emotion and to_emotion:
                    transition = f"{from_emotion}->{to_emotion}"
                    transitions[transition] += 1
                    
            # Find most common transitions
            common_transitions = sorted(
                transitions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            return {
                'detected': True,
                'common_transitions': [
                    {'transition': t[0], 'count': t[1]}
                    for t in common_transitions
                ],
                'total_micro_expressions': len(micro_expressions)
            }
            
        except Exception as e:
            logger.error(f"Error detecting micro-expression pattern: {e}")
            return {'detected': False, 'error': str(e)}
            
    def _detect_spikes(
        self,
        values: List[float],
        threshold: float
    ) -> List[int]:
        """Detect spikes in a time series"""
        spikes = []
        for i in range(1, len(values) - 1):
            if values[i] - values[i-1] > threshold:
                spikes.append(i)
        return spikes
        
    def _align_data(
        self,
        emotion_history: List[Dict],
        performance_metrics: List[Dict]
    ) -> List[Dict]:
        """Align emotion and performance data by timestamp"""
        aligned = []
        
        for emotion in emotion_history:
            emotion_time = emotion.get('timestamp', 0)
            
            # Find closest performance metric
            closest_perf = min(
                performance_metrics,
                key=lambda p: abs(p.get('timestamp', 0) - emotion_time)
            )
            
            time_diff = abs(closest_perf.get('timestamp', 0) - emotion_time)
            
            # Only align if within 1 second
            if time_diff < 1.0:
                aligned.append({
                    'emotion': emotion,
                    'performance': closest_perf,
                    'time_diff': time_diff
                })
                
        return aligned
        
    def _find_optimal_range(
        self,
        feature_values: List[float],
        performance_values: List[float]
    ) -> Dict[str, float]:
        """Find optimal range for a feature"""
        # Sort by performance (assuming lower lap time is better)
        sorted_indices = np.argsort(performance_values)
        top_10_percent = int(len(sorted_indices) * 0.1)
        
        if top_10_percent < 1:
            top_10_percent = 1
            
        best_indices = sorted_indices[:top_10_percent]
        best_features = [feature_values[i] for i in best_indices]
        
        return {
            'min': float(np.min(best_features)),
            'max': float(np.max(best_features)),
            'mean': float(np.mean(best_features)),
            'std': float(np.std(best_features))
        }
        
    def store_pattern(
        self,
        pattern_type: str,
        pattern_data: Dict[str, Any],
        confidence: float
    ):
        """Store a detected pattern"""
        self.patterns[pattern_type].append(pattern_data)
        self.pattern_confidence[pattern_type] = confidence
        logger.info(f"Pattern stored: {pattern_type} (confidence: {confidence:.2f})")
        
    def get_patterns(self, pattern_type: Optional[str] = None) -> Dict:
        """Get stored patterns"""
        if pattern_type:
            return {
                'patterns': self.patterns.get(pattern_type, []),
                'confidence': self.pattern_confidence.get(pattern_type, 0.0)
            }
        return dict(self.patterns)
        
    def clear_patterns(self):
        """Clear all stored patterns"""
        self.patterns.clear()
        self.pattern_confidence.clear()
        logger.info("All patterns cleared")


# Example usage
if __name__ == "__main__":
    from ..utils.logger import setup_logger
    
    setup_logger(__name__, level="DEBUG")
    
    engine = PatternRecognitionEngine()
    
    # Test stress pattern detection
    emotion_history = [
        {'stress_level': 5.0 + i * 0.5, 'timestamp': i}
        for i in range(20)
    ]
    
    telemetry_history = [
        {'speed': 150 + i * 2, 'timestamp': i}
        for i in range(20)
    ]
    
    result = engine.detect_stress_pattern(emotion_history, telemetry_history)
    logger.info(f"Stress pattern detection: {result}")

# Made with Bob
