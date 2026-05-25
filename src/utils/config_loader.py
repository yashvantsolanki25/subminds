"""
Configuration loader utility
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    """Load and manage configuration files"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize config loader
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        load_dotenv()  # Load environment variables from .env
        
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load YAML configuration file
        
        Args:
            filename: Name of the YAML file
            
        Returns:
            Dictionary containing configuration
        """
        filepath = self.config_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
            
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
            
        # Replace environment variable placeholders
        config = self._replace_env_vars(config)
        
        return config
        
    def _replace_env_vars(self, config: Any) -> Any:
        """
        Recursively replace environment variable placeholders
        
        Args:
            config: Configuration dict or value
            
        Returns:
            Configuration with environment variables replaced
        """
        if isinstance(config, dict):
            return {k: self._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._replace_env_vars(item) for item in config]
        elif isinstance(config, str):
            # Replace ${VAR_NAME} or ${VAR_NAME:default}
            if config.startswith("${") and config.endswith("}"):
                var_spec = config[2:-1]
                if ":" in var_spec:
                    var_name, default = var_spec.split(":", 1)
                    return os.getenv(var_name, default)
                else:
                    value = os.getenv(var_spec)
                    if value is None:
                        raise ValueError(f"Environment variable {var_spec} not set")
                    return value
        return config
        
    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all configuration files
        
        Returns:
            Dictionary with all configurations
        """
        configs = {}
        
        config_files = [
            'ibm_granite_config.yaml',
            'torcs_config.yaml',
            'camera_config.yaml',
            'database_config.yaml'
        ]
        
        for filename in config_files:
            config_name = filename.replace('_config.yaml', '')
            try:
                configs[config_name] = self.load_yaml(filename)
            except FileNotFoundError:
                print(f"Warning: {filename} not found, skipping...")
                
        return configs


# Singleton instance
_config_loader = None


def get_config_loader() -> ConfigLoader:
    """Get singleton config loader instance"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader


def load_config(filename: str) -> Dict[str, Any]:
    """
    Convenience function to load a config file
    
    Args:
        filename: Name of the config file
        
    Returns:
        Configuration dictionary
    """
    loader = get_config_loader()
    return loader.load_yaml(filename)

# Made with Bob
