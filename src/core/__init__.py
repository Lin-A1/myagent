"""
Core module for MyAgent project.

This module contains the core functionality including base classes,
engines, and utilities used throughout the application.
"""

from .base import Logger, get_logger, setup_logging

__all__ = ["Logger", "get_logger", "setup_logging"]