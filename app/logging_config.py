import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Define log format for better readability
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger.

    Example:
    >>> logger = get_logger(__name__)
    >>> logger.info("Application started")
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured (avoid duplicate handlers)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

        # Console handler (INFO level and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (DEBUG level and above)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_DIR / "application.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5  # Keep 5 backup files
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def configure_logging(level: str = "INFO") -> None:
    """
    Configure root logger for the application

    Example:
    >>> configure_logging(level="DEBUG")
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level))

    # Get the logger
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "application.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
