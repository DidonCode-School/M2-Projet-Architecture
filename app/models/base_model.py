from app.messaging.event import Event

class BaseModel:

    def __init__(self):
        """Initialise le modèle de base."""
        self.content = None

    def generate_pdf(self):
        """Méthode que les classes filles doivent obligatoirement surcharger pour générer un document PDF."""
        raise NotImplementedError("La méthode generate_pdf() doit être implémentée.")

    def save(self, storage, filename: str, content: bytes):
        """Méthode pour sauvegarder le document généré dans le stockage."""
        storage.save(filename, content)

    def from_event(self, event: Event):
        """Méthode que les classes filles doivent surcharger pour créer une instance à partir d'un événement."""
        raise NotImplementedError("La méthode from_event() doit être implémentée.")