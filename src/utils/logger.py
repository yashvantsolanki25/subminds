"""
Logging utilities for SubMinds
Production-ready logging configuration
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep
        console_output: Whether to output to console
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add file handler if log_file specified
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    # Add console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get existing logger by name
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Example usage
if __name__ == "__main__":
    # Setup logger
    logger = setup_logger('test_logger', 'logs/test.log')
    
    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    
    print("Logging test complete. Check logs/test.log")

# Made with Bob
