from app.models.base_model import BaseModel

class AccessExitDocument(BaseModel):
    def __init__(
        self, 
        vehicle_id: int, 
        place_id: int, 
        has_reservation: bool,
        place_type: str,
        category: int,
    ):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.place_id = place_id
        self.has_reservation = has_reservation
        self.place_type = place_type
        self.category = category

    def generate_pdf(self):
        pass

    def save(self, storage):
        pass