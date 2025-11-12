# utils/logger.py
import logging
from datetime import datetime
from pathlib import Path

def get_logger():
    log_folder = Path("reports/logs")
    log_folder.mkdir(parents=True, exist_ok=True)

    log_file = log_folder / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger("SauceDemoTest")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
