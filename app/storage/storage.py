import logging
import os
from pathlib import Path
from app.core.config import Config

class Storage:

    def __init__(self, path: str = "/"):
        """Initialise le stockage avec un chemin spécifique."""
        self.logger = logging.getLogger(Config.LOGGER_NAME)
        self.root = os.path.abspath("storage")
        self.path = os.path.join(self.root, path.lstrip("/\\"))

        os.makedirs(self.path, exist_ok=True)

    def resolve_file_path(self, sub_path: str, filename: str) -> Path | None:
        """Résout et sécurise le chemin complet d'un fichier dans le stockage."""
        safe_sub = Path(sub_path.lstrip("/\\"))
        safe_name = Path(filename).name
        if not safe_name or safe_name != filename:
            return None

        base_dir = Path(self.path).resolve()
        target_dir = (base_dir / safe_sub).resolve()
        file_path = (target_dir / safe_name).resolve()

        # Empêche toute sortie hors du répertoire de stockage
        if base_dir not in file_path.parents:
            return None

        return file_path

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

    def get(self, path: str, filename: str) -> bytes | None:
        """Récupère le contenu binaire d'un fichier."""
        try:
            file_path = self.resolve_file_path(path, filename)
            if file_path is None or not file_path.is_file():
                return None

            with open(file_path, "rb") as f:
                content = f.read()

            self.logger.info(f"Fichier récupéré : {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Échec de la récupération du fichier : {e}")
            return None