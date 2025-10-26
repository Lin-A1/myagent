"""
Core base module for MyAgent project.

This module contains base classes and utilities for the entire application.
"""

from .logger import Logger, get_logger, setup_logging

__all__ = ["Logger", "get_logger", "setup_logging"]