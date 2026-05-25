"""
IBM Granite AI Client for pattern analysis
Production-ready implementation with comprehensive error handling
"""
import os
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

try:
    from ibm_watson_machine_learning.foundation_models import Model
    from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
    IBM_WML_AVAILABLE = True
except ImportError:
    IBM_WML_AVAILABLE = False
    logging.warning("IBM Watson Machine Learning not available")

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logging.warning("PyYAML not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraniteAIClient:
    """Client for IBM Granite AI model with comprehensive error handling"""
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        url: str = "https://us-south.ml.cloud.ibm.com"
    ):
        """
        Initialize Granite AI client
        
        Args:
            config_path: Path to configuration file (YAML)
            api_key: IBM Cloud API key (overrides config file)
            project_id: IBM Watson Studio project ID (overrides config file)
            url: IBM Watson Machine Learning URL
        """
        self.config_path = config_path
        self.url = url
        self.model: Optional[Any] = None
        self.api_key: Optional[str] = None
        self.project_id: Optional[str] = None
        
        # Load configuration
        if config_path and Path(config_path).exists():
            self.config = self._load_config(config_path)
        else:
            self.config = self._get_default_config()
        
        # Override with direct parameters
        if api_key:
            self.api_key = api_key
        if project_id:
            self.project_id = project_id
        
        # Get from environment if not set
        if not self.api_key:
            self.api_key = os.getenv('IBM_CLOUD_API_KEY')
        if not self.project_id:
            self.project_id = os.getenv('IBM_PROJECT_ID')
        
        # Initialize model if credentials available
        if IBM_WML_AVAILABLE and self.api_key and self.project_id:
            try:
                self.model = self._initialize_model()
                logger.info("IBM Granite client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Granite model: {e}")
                self.model = None
        else:
            logger.warning("IBM Granite not available. Using mock mode.")
            self.model = None
        
        # Request tracking
        self.request_count = 0
        self.error_count = 0
        self.total_tokens = 0
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            if not YAML_AVAILABLE:
                logger.warning("PyYAML not available, using default config")
                return self._get_default_config()
            
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Extract IBM Granite config
            if 'ibm_granite' in config:
                config = config['ibm_granite']
            
            logger.info(f"Configuration loaded from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            'url': self.url,
            'model': {
                'id': 'ibm/granite-13b-chat-v2',
                'version': 'latest'
            },
            'parameters': {
                'max_tokens': 2000,
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 50,
                'repetition_penalty': 1.1
            },
            'rate_limits': {
                'requests_per_minute': 60,
                'tokens_per_minute': 100000,
                'retry_attempts': 3,
                'retry_delay': 2
            }
        }
    
    def _initialize_model(self) -> Any:
        """
        Initialize IBM Granite model
        
        Returns:
            Initialized model instance
        """
        if not IBM_WML_AVAILABLE:
            raise RuntimeError("IBM Watson Machine Learning not available")
        
        if not self.api_key or not self.project_id:
            raise ValueError("API key and project ID are required")
        
        credentials = {
            "url": self.config.get('url', self.url),
            "apikey": self.api_key
        }
        
        model_id = self.config.get('model', {}).get('id', 'ibm/granite-13b-chat-v2')
        
        parameters = {
            GenParams.MAX_NEW_TOKENS: self.config.get('parameters', {}).get('max_tokens', 2000),
            GenParams.TEMPERATURE: self.config.get('parameters', {}).get('temperature', 0.7),
            GenParams.TOP_P: self.config.get('parameters', {}).get('top_p', 0.9),
            GenParams.TOP_K: self.config.get('parameters', {}).get('top_k', 50),
        }
        
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=self.project_id
        )
        
        return model
    
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
            # Create analysis prompt
            prompt = self._create_analysis_prompt(
                facial_data,
                telemetry,
                art_analysis,
                context
            )
            
            # Generate insights
            if self.model:
                response = self._generate_with_retry(prompt)
            else:
                response = self._get_mock_response(facial_data, telemetry)
            
            # Parse response
            insights = self._parse_response(response, facial_data, telemetry)
            
            # Update statistics
            self.request_count += 1
            
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
            self.error_count += 1
            return self._get_error_response(str(e))
    
    def _create_analysis_prompt(
        self,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any],
        art_analysis: Optional[Dict[str, Any]],
        context: Optional[str]
    ) -> str:
        """
        Create analysis prompt for Granite
        
        Args:
            facial_data: Facial expression data
            telemetry: Racing telemetry
            art_analysis: Optional art analysis
            context: Optional context
            
        Returns:
            Formatted prompt string
        """
        prompt = """You are an expert sports psychologist analyzing F1 driver performance.

FACIAL EXPRESSION DATA:
"""
        
        # Add facial data
        if facial_data:
            prompt += f"- Dominant emotion: {facial_data.get('dominant_emotion', 'unknown')}\n"
            prompt += f"- Confidence: {facial_data.get('confidence', 0):.2f}\n"
            prompt += f"- Valence (negative to positive): {facial_data.get('valence', 0):.2f}\n"
            prompt += f"- Arousal (calm to excited): {facial_data.get('arousal', 0):.2f}\n"
        
        # Add telemetry data
        prompt += "\nRACING TELEMETRY:\n"
        if telemetry:
            prompt += f"- Speed: {telemetry.get('speed', 0):.1f} km/h\n"
            prompt += f"- Steering angle: {telemetry.get('steering', 0):.3f}\n"
            prompt += f"- Track position: {telemetry.get('track_position', 0):.3f}\n"
            if 'lap_time' in telemetry:
                prompt += f"- Lap time: {telemetry.get('lap_time', 0):.2f}s\n"
        
        # Add art analysis if available
        if art_analysis:
            prompt += "\nART PSYCHOLOGY ANALYSIS:\n"
            prompt += f"- Dominant colors: {art_analysis.get('dominant_colors', [])}\n"
            prompt += f"- Composition style: {art_analysis.get('composition_style', 'unknown')}\n"
            prompt += f"- Psychological themes: {art_analysis.get('themes', [])}\n"
        
        # Add context if provided
        if context:
            prompt += f"\nADDITIONAL CONTEXT:\n{context}\n"
        
        # Add analysis request
        prompt += """
Based on this multimodal data, provide:
1. Current subconscious emotional state and its impact on performance
2. Identified stress triggers and coping mechanisms
3. Decision-making patterns (conscious vs subconscious)
4. Specific recommendations for mental state optimization
5. Predictive indicators for performance changes

Format your response as structured JSON with keys: emotional_state, stress_analysis, decision_patterns, recommendations, predictions.
"""
        
        return prompt
    
    def _generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None
    ) -> str:
        """
        Generate text with retry logic
        
        Args:
            prompt: Input prompt
            max_retries: Maximum retry attempts
            
        Returns:
            Generated text
        """
        if not self.model:
            raise RuntimeError("Model not initialized")
        
        retries = max_retries if max_retries is not None else self.config.get('rate_limits', {}).get('retry_attempts', 3)
        retry_delay = self.config.get('rate_limits', {}).get('retry_delay', 2)
        
        for attempt in range(retries):
            try:
                response = self.model.generate_text(prompt=prompt)
                return response
                
            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
        
        raise RuntimeError("Max retries exceeded")
    
    def _parse_response(
        self,
        response: str,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse Granite response into structured insights
        
        Args:
            response: Raw response from Granite
            facial_data: Original facial data
            telemetry: Original telemetry data
            
        Returns:
            Structured insights dictionary
        """
        try:
            # Try to parse as JSON
            if '{' in response and '}' in response:
                start = response.index('{')
                end = response.rindex('}') + 1
                json_str = response[start:end]
                parsed = json.loads(json_str)
                
                return {
                    'timestamp': time.time(),
                    'emotional_state': parsed.get('emotional_state', 'Unknown'),
                    'stress_analysis': parsed.get('stress_analysis', 'No analysis available'),
                    'decision_patterns': parsed.get('decision_patterns', []),
                    'recommendations': parsed.get('recommendations', []),
                    'predictions': parsed.get('predictions', []),
                    'raw_response': response,
                    'input_data': {
                        'facial': facial_data,
                        'telemetry': telemetry
                    }
                }
        except Exception as e:
            logger.warning(f"Could not parse JSON response: {e}")
        
        # Fallback to text parsing
        return {
            'timestamp': time.time(),
            'emotional_state': facial_data.get('dominant_emotion', 'unknown'),
            'stress_analysis': f"Stress level: {facial_data.get('stress_level', 'unknown')}",
            'decision_patterns': ['Pattern analysis in progress'],
            'recommendations': ['Continue monitoring'],
            'predictions': ['Insufficient data for predictions'],
            'raw_response': response,
            'input_data': {
                'facial': facial_data,
                'telemetry': telemetry
            }
        }
    
    def _get_mock_response(
        self,
        facial_data: Dict[str, Any],
        telemetry: Dict[str, Any]
    ) -> str:
        """
        Get mock response when Granite is not available
        
        Args:
            facial_data: Facial expression data
            telemetry: Racing telemetry
            
        Returns:
            Mock response string
        """
        emotion = facial_data.get('dominant_emotion', 'neutral')
        valence = facial_data.get('valence', 0.0)
        speed = telemetry.get('speed', 0)
        
        return f"""{{
    "emotional_state": "Driver showing {emotion} emotion with valence {valence:.2f}",
    "stress_analysis": "Moderate stress levels detected. Monitor for changes.",
    "decision_patterns": ["Consistent decision-making at {speed:.1f} km/h"],
    "recommendations": ["Maintain current mental state", "Focus on breathing exercises"],
    "predictions": ["Performance likely to remain stable"]
}}"""
    
    def _get_error_response(self, error_msg: str) -> Dict[str, Any]:
        """
        Get error response
        
        Args:
            error_msg: Error message
            
        Returns:
            Error response dictionary
        """
        return {
            'timestamp': time.time(),
            'error': True,
            'error_message': error_msg,
            'emotional_state': 'Error',
            'stress_analysis': 'Analysis failed',
            'decision_patterns': [],
            'recommendations': ['Retry analysis'],
            'predictions': []
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get client statistics
        
        Returns:
            Statistics dictionary
        """
        success_rate = 0.0
        if self.request_count > 0:
            success_rate = (self.request_count - self.error_count) / self.request_count
        
        return {
            'total_requests': self.request_count,
            'successful_requests': self.request_count - self.error_count,
            'failed_requests': self.error_count,
            'success_rate': success_rate,
            'total_tokens': self.total_tokens,
            'model_available': self.model is not None,
            'ibm_wml_available': IBM_WML_AVAILABLE
        }
    
    def is_available(self) -> bool:
        """
        Check if Granite client is available
        
        Returns:
            True if client is ready to use
        """
        return self.model is not None
    
    def reset_statistics(self) -> None:
        """Reset statistics counters"""
        self.request_count = 0
        self.error_count = 0
        self.total_tokens = 0
        logger.info("Statistics reset")


# Example usage
if __name__ == "__main__":
    print("Testing IBM Granite AI Client...")
    
    try:
        # Initialize client
        client = GraniteAIClient(
            config_path='config/ibm_granite_config.yaml'
        )
        
        print(f"Client available: {client.is_available()}")
        
        # Test data
        facial_data = {
            'dominant_emotion': 'focused',
            'confidence': 0.85,
            'valence': 0.3,
            'arousal': 0.7,
            'stress_level': 6
        }
        
        telemetry = {
            'speed': 180.5,
            'steering': -0.3,
            'track_position': 0.1,
            'lap_time': 95.3
        }
        
        # Analyze patterns
        print("\nAnalyzing subconscious patterns...")
        insights = client.analyze_subconscious_patterns(
            facial_data=facial_data,
            telemetry=telemetry
        )
        
        print("\nInsights:")
        print(f"Emotional State: {insights.get('emotional_state')}")
        print(f"Stress Analysis: {insights.get('stress_analysis')}")
        print(f"Recommendations: {insights.get('recommendations')}")
        
        # Print statistics
        stats = client.get_statistics()
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
