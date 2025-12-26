"""Logging configuration for the booking system."""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """
    Set up logging with rotating file handler.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("booking_system")
    logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler with rotation (100MB max, rotate after 24 hours)
    log_filename = os.path.join("logs", "booking_system.log")
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=100 * 1024 * 1024,  # 100MB
        backupCount=7,  # Keep 7 backup files (roughly a week)
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(detailed_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger() -> logging.Logger:
    """Get the configured logger instance."""
    return logging.getLogger("booking_system")
