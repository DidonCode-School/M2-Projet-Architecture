import logging
import os

from app.core.config import Config

def load_logger():
    # Création du dossier logs
    os.makedirs(Config.LOG_DIR, exist_ok=True)

    # Création du logger
    logger = logging.getLogger(Config.LOGGER_NAME)
    logger.setLevel(Config.LOG_LEVEL)

    # Éviter les handlers en double
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        Config.LOG_FORMAT,
        datefmt=Config.DATE_FORMAT
    )

    # Handler fichier
    file_handler = logging.FileHandler(
        os.path.join(Config.LOG_DIR, Config.LOG_FILE),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Ajout des handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger