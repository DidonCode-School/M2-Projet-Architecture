import requests
import datetime
from fpdf import FPDF
from app.core.config import Config
from app.messaging.event import Event
from app.models.base_model import BaseModel

class AccessEntryDocument(BaseModel):
    def __init__(
        self,
        event_id: int,
        vehicle_plate: int,
        place_id: int,
        has_reservation: bool,
        place_type: dict,
        category: int,
        created_at: datetime.datetime,
        event_name: str = "Parking",
    ):
        """Initialise les attributs du document d'entrée de parking."""
        super().__init__()
        self.event_id = event_id
        self.vehicle_plate = vehicle_plate
        self.place_id = place_id
        self.has_reservation = has_reservation
        self.place_type = place_type or {}
        self.category = category
        self.created_at = created_at
        self.event_name = event_name

    def generate_pdf(self):
        """Génère un ticket d'entrée de parking au format PDF (bytes)."""

        pdf = FPDF(unit="mm", format=(80, 105))
        pdf.set_margins(6, 6, 6)
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()

        # Palette monochrome
        black = (35, 35, 35)
        grey = (115, 115, 115)
        light_grey = (240, 240, 240)
        border_grey = (210, 210, 210)

        # =============================
        # TYPE DE TICKET
        # =============================

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 11)

        pdf.cell(
            0,
            6,
            "TICKET D'ENTREE",
            align="C",
            ln=1,
        )

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 8)

        pdf.cell(
            0,
            5,
            "ENTREE AUTORISEE",
            align="C",
            ln=1,
        )

        pdf.ln(4)

        # =============================
        # DATE ET HEURE
        # =============================

        date_y = pdf.get_y()

        pdf.set_fill_color(*light_grey)
        pdf.rect(6, date_y, 68, 17, style="F")

        pdf.set_xy(6, date_y + 1)

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 7)

        pdf.cell(
            62,
            6,
            "DATE ET HEURE D'ENTREE",
        )

        pdf.set_xy(6, date_y + 7)

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 11)

        pdf.cell(
            68,
            7,
            self.created_at.strftime("%d/%m/%Y  %H:%M"),
            align="C",
        )

        pdf.set_y(date_y + 17)

        # =============================
        # VEHICULE
        # =============================

        pdf.ln(2)

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 7)

        pdf.cell(
            0,
            4,
            "VEHICULE",
        )

        pdf.ln(2)

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 8)

        pdf.cell(
            0,
            8,
            f"PLAQUE : {self.vehicle_plate}",
        )

        # =============================
        # EMPLACEMENT
        # =============================

        pdf.ln(8)

        place_y = pdf.get_y()

        pdf.set_draw_color(*border_grey)

        pdf.rect(
            6,
            place_y,
            68,
            15,
        )

        pdf.set_xy(6, place_y + 3)

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 7)

        pdf.cell(
            68,
            4,
            "VOTRE EMPLACEMENT",
            align="C",
        )

        pdf.set_xy(6, place_y + 4)

        place_name = "Standard"
        
        if self.place_type.get("isElectric"):
            place_name = "Électrique"

        if self.place_type.get("isHandicap"):
            place_name = "Handicapé"

        if self.place_type.get("isXl"):
            place_name = "XL"

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 10)

        pdf.cell(
            68,
            11,
            place_name,
            align="C",
        )

        pdf.set_y(place_y + 18)

        # =============================
        # DETAILS DU STATIONNEMENT
        # =============================

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 8)

        pdf.cell(
            0,
            5,
            "DETAILS DU STATIONNEMENT",
        )

        pdf.ln(6)

        details = [
            ("Categorie", str(self.category)),
            (
                "Reservation",
                "Oui" if self.has_reservation else "Non",
            ),
        ]

        for label, value in details:

            pdf.set_text_color(*grey)
            pdf.set_font("Helvetica", "", 8)

            pdf.cell(
                30,
                5,
                label,
            )

            pdf.set_text_color(*black)
            pdf.set_font("Helvetica", "B", 8)

            pdf.cell(
                38,
                5,
                value,
                align="R",
            )

            pdf.ln(6)

        # =============================
        # PIED DE PAGE
        # =============================

        pdf.ln(2)

        pdf.set_draw_color(*border_grey)

        pdf.line(
            6,
            pdf.get_y(),
            74,
            pdf.get_y(),
        )

        pdf.ln(4)

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 7)

        pdf.cell(
            0,
            4,
            "Conservez ce ticket jusqu'a votre sortie.",
            align="C",
        )

        pdf.ln(4)

        pdf.set_font("Courier", "", 6)

        pdf.cell(
            0,
            3,
            f"REFERENCE : {self.event_id}",
            align="C",
        )

        self.content = pdf.output(dest="S").encode("latin-1")

        return self.content

    def save(self, storage):
        """Méthode pour sauvegarder le document généré dans le stockage."""
        return storage.save(
            path="access/entrys",
            filename=f"{self.event_id}.pdf",
            content=self.content
        )

    @staticmethod
    def from_event(event: Event):
        """Crée une instance de AccessEntryDocument à partir d'un événement."""

        payload = event.get("payload") or {}
        place_type = payload.get("placeType") or {}

        created_at = event.get("createdAt")

        if isinstance(created_at, str):
            created_at = datetime.datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            )

        try:
            response = requests.get(
                f"{Config.VEHICLE_SERVICE_URL}/api/vehicle/{payload.get('vehicleId')}/plate",
                timeout=(5.0, 120.0),
            )
            response.raise_for_status()
            vehicle_plate = response.text

            return AccessEntryDocument(
                event_id=event.get("id"),
                vehicle_plate=vehicle_plate,
                place_id=payload.get("placeId"),
                has_reservation=payload.get("reservation", False),
                place_type=place_type,
                category=place_type.get("category", 0),
                created_at=created_at,
            )
        except requests.RequestException as exc:
            print(f"Échec de la requête : {exc}")