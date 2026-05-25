"""
IBM Granite AI Client for pattern analysis
"""
import os
import time
from typing import Dict, Any, List, Optional
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

from ..utils.logger import get_logger
from ..utils.config_loader import load_config

logger = get_logger(__name__)


class GraniteAIClient:
    """Client for IBM Granite AI model"""
    
    def __init__(self, config_path: str = "config/ibm_granite_config.yaml"):
        """
        Initialize Granite AI client
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("Initializing IBM Granite AI Client")
        self.config = self._load_config(config_path)
        self.model = self._initialize_model()
        self.request_count = 0
        self.last_request_time = 0
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            full_config = load_config(config_path)
            config = full_config.get('ibm_granite', {})
            
            # Validate required fields
            required_fields = ['api_key', 'url', 'project_id']
            for field in required_fields:
                if not config.get(field):
                    raise ValueError(f"Missing required config field: {field}")
                    
            logger.info("Configuration loaded successfully")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
            
    def _initialize_model(self) -> Model:
        """Initialize IBM Granite model"""
        try:
            credentials = {
                "url": self.config['url'],
                "apikey": self.config['api_key']
            }
            
            model_config = self.config.get('model', {})
            model_id = model_config.get('id', 'ibm/granite-13b-chat-v2')
            project_id = self.config['project_id']
            
            params_config = self.config.get('parameters', {})
            parameters = {
                GenParams.MAX_NEW_TOKENS: params_config.get('max_tokens', 2000),
                GenParams.TEMPERATURE: params_config.get('temperature', 0.7),
                GenParams.TOP_P: params_config.get('top_p', 0.9),
                GenParams.TOP_K: params_config.get('top_k', 50),
            }
            
            model = Model(
                model_id=model_id,
                params=parameters,
                credentials=credentials,
                project_id=project_id
            )
            
            logger.info(f"IBM Granite model initialized: {model_id}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise
            
    def _check_rate_limit(self):
        """Check and enforce rate limits"""
        rate_limits = self.config.get('rate_limits', {})
        rpm = rate_limits.get('requests_per_minute', 60)
        
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Enforce minimum time between requests
        min_interval = 60.0 / rpm
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
        self.request_count += 1
        
    def analyze_subconscious_patterns(
        self,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any],
        art_analysis: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze subconscious patterns using multimodal data
        
        Args:
            facial_data: Facial expression analysis results
            telemetry: Racing telemetry data
            art_analysis: Optional art psychology analysis
            context: Optional additional context
            
        Returns:
            Dictionary containing insights and recommendations
        """
        try:
            self._check_rate_limit()
            
            prompt = self._create_analysis_prompt(
                facial_data,
                telemetry,
                art_analysis,
                context
            )
            
            logger.debug("Sending request to IBM Granite")
            response = self.model.generate_text(prompt=prompt)
            
            insights = self._parse_response(response)
            insights['request_id'] = self.request_count
            
            logger.info(f"Analysis complete (request #{self.request_count})")
            return insights
            
        except Exception as e:
            logger.error(f"Error in pattern analysis: {e}")
            return {
                'error': str(e),
                'raw_response': None,
                'timestamp': time.time()
            }
            
    def _create_analysis_prompt(
        self,
        facial_data: Dict,
        telemetry: Dict,
        art_analysis: Optional[Dict],
        context: Optional[str]
    ) -> str:
        """Create analysis prompt for Granite"""
        
        # Get prompt template
        prompts = self.config.get('prompts', {})
        base_prompt = prompts.get('analysis', 
            "You are an expert sports psychologist analyzing F1 driver performance.")
        
        prompt = f"""{base_prompt}

FACIAL EXPRESSION DATA:
- Dominant emotion: {facial_data.get('dominant_emotion', 'unknown')}
- Confidence: {facial_data.get('confidence', 0):.2f}
- Stress level: {facial_data.get('stress_level', 0):.1f}/10
- Valence (negative to positive): {facial_data.get('valence', 0):.2f}
- Arousal (calm to excited): {facial_data.get('arousal', 0):.2f}

RACING TELEMETRY:
- Speed: {telemetry.get('speed', 0):.1f} km/h
- Steering angle: {telemetry.get('steering', 0):.3f}
- Track position: {telemetry.get('track_position', 0):.3f}
- Lap time: {telemetry.get('lap_time', 0):.2f}s
"""
        
        if art_analysis:
            prompt += f"""
ART PSYCHOLOGY ANALYSIS:
- Dominant colors: {', '.join(art_analysis.get('dominant_colors', []))}
- Composition style: {art_analysis.get('composition_style', 'unknown')}
- Psychological themes: {', '.join(art_analysis.get('themes', []))}
- Stress indicators: {art_analysis.get('stress_indicators', 'none')}
"""
        
        if context:
            prompt += f"\nADDITIONAL CONTEXT:\n{context}\n"
        
        prompt += """
Based on this multimodal data, provide a comprehensive analysis including:

1. CURRENT SUBCONSCIOUS STATE:
   - Emotional state and its impact on performance
   - Stress level assessment
   - Mental readiness indicators

2. DECISION-MAKING PATTERNS:
   - Conscious vs subconscious influences
   - Risk-taking tendencies
   - Response patterns under pressure

3. PERFORMANCE INSIGHTS:
   - Optimal mental state indicators
   - Areas of concern
   - Strengths to leverage

4. RECOMMENDATIONS:
   - Immediate mental state adjustments
   - Training focus areas
   - Stress management strategies

5. PREDICTIVE INDICATORS:
   - Early warning signs
   - Performance trajectory
   - Intervention points

Provide your analysis in a structured, actionable format.
"""
        
        return prompt
        
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse Granite response into structured insights"""
        return {
            'raw_response': response,
            'timestamp': time.time(),
            'analysis_complete': True
        }
        
    def correlate_emotions_performance(
        self,
        emotion_history: List[Dict],
        performance_history: List[Dict]
    ) -> Dict[str, Any]:
        """
        Correlate emotional states with performance metrics
        
        Args:
            emotion_history: List of emotion records
            performance_history: List of performance records
            
        Returns:
            Correlation analysis results
        """
        try:
            self._check_rate_limit()
            
            prompt = self._create_correlation_prompt(
                emotion_history,
                performance_history
            )
            
            response = self.model.generate_text(prompt=prompt)
            
            return {
                'correlations': response,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {e}")
            return {'error': str(e)}
            
    def _create_correlation_prompt(
        self,
        emotion_history: List[Dict],
        performance_history: List[Dict]
    ) -> str:
        """Create correlation analysis prompt"""
        
        prompt = """Analyze the correlation between emotional states and racing performance.

EMOTION HISTORY (last 10 records):
"""
        for i, record in enumerate(emotion_history[-10:]):
            prompt += f"{i+1}. {record.get('dominant_emotion')} (valence: {record.get('valence', 0):.2f})\n"
            
        prompt += "\nPERFORMANCE HISTORY (last 10 records):\n"
        for i, record in enumerate(performance_history[-10:]):
            prompt += f"{i+1}. Lap: {record.get('lap_time', 0):.2f}s, Speed: {record.get('avg_speed', 0):.1f} km/h\n"
            
        prompt += """
Identify:
1. Correlations between emotions and performance
2. Optimal emotional states for peak performance
3. Emotional patterns that predict performance dips
4. Recommendations for emotional regulation
"""
        
        return prompt
        
    def predict_performance(
        self,
        current_state: Dict[str, Any],
        historical_patterns: List[Dict]
    ) -> Dict[str, Any]:
        """
        Predict future performance based on current state
        
        Args:
            current_state: Current driver state
            historical_patterns: Historical pattern data
            
        Returns:
            Performance predictions
        """
        try:
            self._check_rate_limit()
            
            prompt = f"""Based on the current driver state and historical patterns, predict performance.

CURRENT STATE:
- Emotion: {current_state.get('emotion')}
- Stress: {current_state.get('stress', 0):.1f}/10
- Valence: {current_state.get('valence', 0):.2f}
- Arousal: {current_state.get('arousal', 0):.2f}

HISTORICAL PATTERNS:
{len(historical_patterns)} patterns identified

Predict:
1. Expected performance level (1-10)
2. Risk factors
3. Recommended interventions
4. Confidence in prediction
"""
            
            response = self.model.generate_text(prompt=prompt)
            
            return {
                'prediction': response,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error in performance prediction: {e}")
            return {'error': str(e)}
            
    def get_request_stats(self) -> Dict[str, Any]:
        """Get client usage statistics"""
        return {
            'total_requests': self.request_count,
            'last_request_time': self.last_request_time,
            'model_id': self.config.get('model', {}).get('id')
        }


# Example usage
if __name__ == "__main__":
    from ..utils.logger import setup_logger
    
    setup_logger(__name__, level="DEBUG")
    
    try:
        client = GraniteAIClient()
        
        # Test analysis
        facial_data = {
            'dominant_emotion': 'focused',
            'confidence': 0.85,
            'stress_level': 6.5,
            'valence': 0.3,
            'arousal': 0.7
        }
        
        telemetry = {
            'speed': 180.5,
            'steering': -0.3,
            'track_position': 0.1,
            'lap_time': 95.3
        }
        
        insights = client.analyze_subconscious_patterns(facial_data, telemetry)
        logger.info(f"Analysis result: {insights}")
        
        # Get stats
        stats = client.get_request_stats()
        logger.info(f"Client stats: {stats}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)

# Made with Bob
