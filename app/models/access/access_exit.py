import datetime
from fpdf import FPDF
import requests
from app.core.config import Config
from app.models.base_model import BaseModel
from app.messaging.event import Event

class AccessExitDocument(BaseModel):
    def __init__(
        self, 
        event_id: str,
        vehicle_plate: str,
        place_id: str,
        amount: float,  
        payment_id: str,
        created_at: datetime.datetime,
    ):
        super().__init__()
        self.event_id = event_id
        self.vehicle_plate = vehicle_plate
        self.place_id = place_id
        self.amount = amount
        self.payment_id = payment_id
        self.created_at = created_at

    def generate_pdf(self):
        """Génère un ticket de sortie de parking au format PDF (bytes)."""

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
            "TICKET DE SORTIE",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 8)

        pdf.cell(
            0,
            5,
            "SORTIE AUTORISEE",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(4)

        # =============================
        # DATE ET HEURE DE SORTIE
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
            "DATE ET HEURE DE SORTIE",
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
        # PAIEMENT
        # =============================

        pdf.ln(8)

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 8)

        pdf.cell(
            0,
            5,
            "DETAILS DU PAIEMENT",
        )

        pdf.ln(6)

        # Montant payé
        pdf.set_fill_color(*light_grey)

        amount_y = pdf.get_y()

        pdf.rect(
            6,
            amount_y,
            68,
            15,
            style="F",
        )

        pdf.set_xy(9, amount_y + 2)

        pdf.set_text_color(*grey)
        pdf.set_font("Helvetica", "", 7)

        pdf.cell(
            62,
            4,
            "MONTANT PAYE",
        )

        pdf.set_xy(9, amount_y + 6)

        pdf.set_text_color(*black)
        pdf.set_font("Helvetica", "B", 13)

        pdf.cell(
            62,
            7,
            f"{self.amount:.2f} EUR",
        )

        pdf.set_y(amount_y + 15)

        pdf.ln(3)

        details = [
            ("Statut", "PAYE"),
            ("Paiement", self.payment_id),
        ]

        for label, value in details:

            pdf.set_text_color(*grey)
            pdf.set_font("Helvetica", "", 7)

            pdf.cell(
                25,
                5,
                label,
            )

            pdf.set_text_color(*black)
            pdf.set_font("Helvetica", "B", 7)

            pdf.cell(
                43,
                5,
                str(value)[:30],
                align="R",
            )

            pdf.ln(5)

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
            "Merci de votre visite.",
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

        self.content = bytes(pdf.output())

        return self.content
    
    def save(self, storage):
        """Méthode pour sauvegarder le document généré dans le stockage."""
        return storage.save(
            path="access/exits",
            filename=f"{self.event_id}.pdf",
            content=self.content
        )

    @staticmethod
    def from_event(event: Event):
        """Crée une instance de AccessExitDocument à partir d'un événement."""
        
        payload = event.get("payload") or {}
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

            return AccessExitDocument(
                event_id=event.get("id"),
                vehicle_plate=vehicle_plate,
                place_id=payload.get("placeId"),
                amount=float(payload.get("amount") or 0),
                payment_id=payload.get("paymentId"),
                created_at=created_at,
            )
        except requests.RequestException as exc:
            print(f"Échec de la requête : {exc}")