import logging
import os
from app.config import settings

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def _setup_dir():
    log_dir = os.path.dirname(os.path.abspath(settings.TARGET_LOG_FILE_PATH))
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

def _get_root_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    
    return root_logger

def setup_logging():
    _setup_dir()

    root_logger = _get_root_logger()

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel( getattr(logging, settings.LOG_LEVEL_STDOUT.upper()) )
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(settings.TARGET_LOG_FILE_PATH, encoding="utf-8")
    file_handler.setLevel( getattr(logging, settings.LOG_LEVEL_FILE.upper()) )
    file_handler.setFormatter(formatter)
    
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)

    return root_logger

logger = setup_logging()