import logging
import os
from app.core.config import Config

class Storage:

    def __init__(self, path: str = "/"):
        """Initialise le stockage avec un chemin spécifique."""
        self.logger = logging.getLogger(Config.LOGGER_NAME)
        self.root = os.path.abspath("storage")
        self.path = os.path.join(self.root, path.lstrip("/\\"))

        os.makedirs(self.path, exist_ok=True)

    def save(self, path: str, filename: str, content: bytes):
        """Enregistre le contenu binaire dans un fichier."""
        try:
            path = path.lstrip("/\\")

            directory = os.path.join(self.path, path)
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, filename)

            with open(file_path, "wb") as f:
                f.write(content)

            self.logger.info(f"Fichier enregistré : {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Échec de l'enregistrement du fichier : {e}")