"""
Logger configuration and utilities for MyAgent project.

This module provides a centralized logging system with support for:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File rotation and size management
- Structured logging with JSON format
- Different log categories (app, error, debug, access)
- Thread-safe logging operations
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string.
        
        Args:
            record: The log record to format.
            
        Returns:
            JSON formatted log string.
        """
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
            
        return json.dumps(log_entry, ensure_ascii=False)


class Logger:
    """Enhanced logger class with multiple handlers and formatters."""
    
    _instances: Dict[str, logging.Logger] = {}
    _initialized: bool = False
    
    @classmethod
    def setup_logging(
        cls,
        log_level: Union[str, int] = logging.INFO,
        log_dir: Optional[Union[str, Path]] = None,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        enable_console: bool = True,
        enable_json_format: bool = False,
    ) -> None:
        """Setup global logging configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            log_dir: Directory to store log files. Defaults to 'logs' in project root.
            max_file_size: Maximum size of each log file in bytes.
            backup_count: Number of backup files to keep.
            enable_console: Whether to enable console logging.
            enable_json_format: Whether to use JSON format for file logs.
        """
        if cls._initialized:
            return
            
        # Determine log directory
        if log_dir is None:
            # Find project root (assuming this file is in src/core/base/)
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent.parent
            log_dir = project_root / "logs"
        else:
            log_dir = Path(log_dir)
            
        # Create log directories
        log_dir.mkdir(exist_ok=True)
        for subdir in ["app", "error", "debug", "access"]:
            (log_dir / subdir).mkdir(exist_ok=True)
            
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Setup formatters
        console_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        file_formatter = JSONFormatter() if enable_json_format else logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
            
        # File handlers for different log types
        handlers_config = [
            ("app", log_dir / "app" / "app.log", logging.INFO),
            ("error", log_dir / "error" / "error.log", logging.ERROR),
            ("debug", log_dir / "debug" / "debug.log", logging.DEBUG),
        ]
        
        for handler_name, log_file, min_level in handlers_config:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=max_file_size,
                backupCount=backup_count,
                encoding="utf-8"
            )
            file_handler.setLevel(min_level)
            file_handler.setFormatter(file_formatter)
            
            # Add filter to ensure only appropriate levels go to each file
            if handler_name == "error":
                file_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
            elif handler_name == "app":
                file_handler.addFilter(lambda record: logging.INFO <= record.levelno < logging.ERROR)
            elif handler_name == "debug":
                file_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
                
            root_logger.addHandler(file_handler)
            
        cls._initialized = True
        
        # Log initialization message
        logger = cls.get_logger("Logger")
        logger.info("Logging system initialized successfully")
        logger.info(f"Log directory: {log_dir}")
        logger.info(f"Log level: {logging.getLevelName(log_level)}")
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger instance.
        
        Args:
            name: Logger name, typically the module name.
            
        Returns:
            Logger instance.
        """
        if name not in cls._instances:
            logger = logging.getLogger(name)
            cls._instances[name] = logger
            
        return cls._instances[name]
    
    @classmethod
    def log_access(cls, message: str, **kwargs) -> None:
        """Log access information to dedicated access log.
        
        Args:
            message: Log message.
            **kwargs: Additional fields to include in log.
        """
        logger = cls.get_logger("ACCESS")
        
        # Add extra fields if provided
        if kwargs:
            # Create a custom LogRecord with extra fields
            record = logger.makeRecord(
                logger.name, logging.INFO, __file__, 0, message, (), None
            )
            record.extra_fields = kwargs
            logger.handle(record)
        else:
            logger.info(message)


# Convenience functions
def setup_logging(**kwargs) -> None:
    """Setup logging with default configuration.
    
    Args:
        **kwargs: Arguments to pass to Logger.setup_logging().
    """
    Logger.setup_logging(**kwargs)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name.
        
    Returns:
        Logger instance.
    """
    return Logger.get_logger(name)


# Auto-setup logging when module is imported
if not Logger._initialized:
    setup_logging()