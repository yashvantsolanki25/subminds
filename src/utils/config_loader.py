"""
Configuration loader for SubMinds
Handles YAML configuration files with environment variable substitution
"""
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
import logging

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logging.warning("PyYAML not available. Install with: pip install pyyaml")

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage configuration files"""
    
    def __init__(self, config_dir: str = 'config'):
        """
        Initialize config loader
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Dict[str, Any]] = {}
        
    def load(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_file: Configuration file name or path
            
        Returns:
            Configuration dictionary
        """
        if not YAML_AVAILABLE:
            logger.error("PyYAML not available")
            return {}
        
        try:
            # Resolve path
            if Path(config_file).is_absolute():
                config_path = Path(config_file)
            else:
                config_path = self.config_dir / config_file
            
            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                return {}
            
            # Load YAML
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Substitute environment variables
            content = self._substitute_env_vars(content)
            
            # Parse YAML
            config = yaml.safe_load(content)
            
            # Cache config
            self.configs[config_file] = config
            
            logger.info(f"Configuration loaded from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config {config_file}: {e}")
            return {}
    
    def _substitute_env_vars(self, content: str) -> str:
        """
        Substitute environment variables in config content
        
        Supports formats:
        - ${VAR_NAME}
        - ${VAR_NAME:default_value}
        
        Args:
            content: Configuration file content
            
        Returns:
            Content with substituted variables
        """
        # Pattern: ${VAR_NAME} or ${VAR_NAME:default}
        pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
        
        def replace(match):
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) is not None else ''
            return os.getenv(var_name, default_value)
        
        return re.sub(pattern, replace, content)
    
    def get(self, config_file: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            config_file: Configuration file name
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        # Load config if not cached
        if config_file not in self.configs:
            self.load(config_file)
        
        config = self.configs.get(config_file, {})
        
        # Support dot notation (e.g., 'database.host')
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def reload(self, config_file: str) -> Dict[str, Any]:
        """
        Reload configuration file
        
        Args:
            config_file: Configuration file name
            
        Returns:
            Reloaded configuration
        """
        if config_file in self.configs:
            del self.configs[config_file]
        return self.load(config_file)
    
    def get_all(self, config_file: str) -> Dict[str, Any]:
        """
        Get entire configuration
        
        Args:
            config_file: Configuration file name
            
        Returns:
            Complete configuration dictionary
        """
        if config_file not in self.configs:
            self.load(config_file)
        return self.configs.get(config_file, {})


# Global config loader instance
_config_loader: Optional[ConfigLoader] = None


def get_config_loader(config_dir: str = 'config') -> ConfigLoader:
    """
    Get global config loader instance
    
    Args:
        config_dir: Configuration directory
        
    Returns:
        ConfigLoader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader(config_dir)
    return _config_loader


def load_config(config_file: str, config_dir: str = 'config') -> Dict[str, Any]:
    """
    Convenience function to load configuration
    
    Args:
        config_file: Configuration file name
        config_dir: Configuration directory
        
    Returns:
        Configuration dictionary
    """
    loader = get_config_loader(config_dir)
    return loader.load(config_file)


# Example usage
if __name__ == "__main__":
    # Set test environment variable
    os.environ['TEST_VAR'] = 'test_value'
    
    # Create test config
    test_config_dir = Path('test_config')
    test_config_dir.mkdir(exist_ok=True)
    
    test_config_file = test_config_dir / 'test.yaml'
    test_config_file.write_text("""
database:
  host: ${DB_HOST:localhost}
  port: 5432
  user: ${DB_USER:admin}
  password: ${DB_PASSWORD:secret}

app:
  name: SubMinds
  version: 1.0.0
  debug: ${DEBUG:false}
  test_var: ${TEST_VAR}
""")
    
    # Load config
    loader = ConfigLoader('test_config')
    config = loader.load('test.yaml')
    
    print("Loaded configuration:")
    print(config)
    
    # Test get method
    print(f"\nDatabase host: {loader.get('test.yaml', 'database.host')}")
    print(f"App name: {loader.get('test.yaml', 'app.name')}")
    print(f"Test var: {loader.get('test.yaml', 'app.test_var')}")
    
    # Cleanup
    test_config_file.unlink()
    test_config_dir.rmdir()
    
    print("\nConfig loader test complete")

# Made with Bob
