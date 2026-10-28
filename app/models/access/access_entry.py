from datetime import datetime
from fpdf import FPDF
from app.models.base_model import BaseModel

class AccessEntryDocument(BaseModel):
    def __init__(
        self, 
        event_id: int,
        vehicle_id: int, 
        place_id: int, 
        has_reservation: bool,
        place_type: str,
        category: int,
        created_at: datetime,
    ):
        """Initialise les attributs du document d'entrée de parking."""
        super().__init__()
        self.event_id = event_id
        self.vehicle_id = vehicle_id
        self.place_id = place_id
        self.has_reservation = has_reservation
        self.place_type = place_type
        self.category = category
        self.created_at = created_at

    def generate_pdf(self):
        pass

    def save(self, storage):
        pass