import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path("../logs/app.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Create the logger
LOGGER = logging.getLogger("app_logger")
LOGGER.setLevel(logging.INFO)

# File logger with rotation (5MB each, keep 5 backups)
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5_000_000,
    backupCount=5,
)
file_handler.setLevel(logging.INFO)

# Formatter: timestamp | level | message
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

file_handler.setFormatter(formatter)
LOGGER.addHandler(file_handler)


def get_logger():
    return LOGGER
