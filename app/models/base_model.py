class BaseModel:

    # Constructeur de la classe de base pour les modèles de documents
    def __init__(self):
        pass

    # Méthode que les classes filles doivent obligatoirement surcharger pour générer un PDF
    def generate_pdf(self):
        """Méthode que les classes filles doivent obligatoirement surcharger"""
        raise NotImplementedError("La méthode generate_pdf() doit être implémentée.")
