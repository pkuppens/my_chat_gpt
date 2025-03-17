"""
Logging configuration module for standardized application logging.

This module provides a configured logger with customizable log levels,
formatters, and handlers for both console and file output.
It handles environment variable detection for buffering control and
ensures proper context information (filename, line number) in logs.
"""

import logging
import os
from typing import Optional, Union, Literal, Dict, List


def configure_logger(
    name: Optional[str] = None,
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    include_file_info: bool = True,
    force_unbuffered: bool = False,
    add_file_handler: bool = False,
    log_file_path: Optional[str] = None,
    log_file_level: Union[int, str] = logging.INFO,
) -> logging.Logger:
    """
    Configure and return a logger with specified settings.

    Args:
        name: The logger name. If None, uses the caller's module name.
        level: The minimum logging level for the console handler.
            Can be a string ('DEBUG', 'INFO', etc.) or a logging constant.
        format_string: Custom format string for log messages. If None, uses a default format.
        include_file_info: Whether to include filename and line number in log messages.
        force_unbuffered: Force Python's stdout to be unbuffered regardless of environment settings.
        add_file_handler: Whether to add a file handler in addition to console handler.
        log_file_path: Path to log file when using file handler. 
            If None and add_file_handler is True, uses "application.log".
        log_file_level: Minimum logging level for the file handler.
            Can be a string ('DEBUG', 'INFO', etc.) or a logging constant.

    Returns:
        A configured logging.Logger instance.

    Example:
        >>> logger = configure_logger(level="DEBUG", include_file_info=True)
        >>> logger.info("Application started")
        2025-03-17 14:30:22,531 - INFO - [main.py:45] - Application started
    """
    # Handle Python output buffering
    if force_unbuffered or os.environ.get("PYTHONUNBUFFERED", "").lower() in ("1", "true"):
        # Force stdout to be unbuffered
        import sys
        if hasattr(sys.stdout, 'reconfigure'):  # Python 3.7+
            sys.stdout.reconfigure(line_buffering=False)
            sys.stderr.reconfigure(line_buffering=False)

    # Determine the logger name
    logger_name = name if name is not None else __name__

    # Create or get the logger
    logger = logging.getLogger(logger_name)
    
    # Clear any existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Set the logger's level
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    logger.setLevel(level)

    # Determine format string with or without file info
    if format_string is None:
        if include_file_info:
            format_string = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        else:
            format_string = "%(asctime)s - %(levelname)s - %(message)s"

    # Create formatter
    formatter = logging.Formatter(format_string)

    # Create and add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # Optionally add file handler
    if add_file_handler:
        file_path = log_file_path or "application.log"
        if isinstance(log_file_level, str):
            log_file_level = getattr(logging, log_file_level.upper())
            
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_file_level)
        logger.addHandler(file_handler)

    return logger


# Default application logger
logger = configure_logger(
    name=__name__,
    level=os.environ.get("LOG_LEVEL", "INFO"),
    include_file_info=True,
)


class LoggerContext:
    """
    Context manager for temporarily changing logger levels.
    
    Allows temporarily changing the logging level within a specific block of code,
    automatically restoring the previous level when exiting the context.
    
    Example:
        >>> with LoggerContext(logger, logging.DEBUG):
        ...     logger.debug("This will be logged only within this context")
    """
    
    def __init__(self, target_logger: logging.Logger, level: Union[int, str]):
        """
        Initialize a logger context with specified logger and temporary level.
        
        Args:
            target_logger: The logger to modify.
            level: The logging level to temporarily apply.
        """
        self.logger = target_logger
        if isinstance(level, str):
            self.level = getattr(logging, level.upper())
        else:
            self.level = level
        self.previous_level = target_logger.level
        
    def __enter__(self) -> logging.Logger:
        """Set temporary logging level and return the logger."""
        self.logger.setLevel(self.level)
        return self.logger
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Restore the original logging level."""
        self.logger.setLevel(self.previous_level)
