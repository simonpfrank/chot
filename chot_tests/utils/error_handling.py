"""
Utility module for handling errors and providing debugging information.

This module contains utility functions for error handling and debugging.
"""

import logging
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")


def setup_logging(level: int = logging.INFO) -> None:
    """Set up logging configuration.

    Args:
        level: The logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def safe_execute(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Execute a function safely with error handling.

    Args:
        func: The function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        The return value of the function

    Raises:
        Exception: If the function execution fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error executing {func.__name__}: {str(e)}")
        raise
