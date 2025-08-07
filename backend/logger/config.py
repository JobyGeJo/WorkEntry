import os
from logging.handlers import RotatingFileHandler
import logging

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_rotating_handler(filename: str, level=logging.DEBUG):
    handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, filename),
        maxBytes=1_000_000,
        backupCount=5
    )
    formatter = logging.Formatter(
        f"[%(levelname)s]: [%(asctime)s] - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler
