from app.models.base_model import BaseModel
from app.messaging.event import Event
from fpdf import FPDF
import datetime

class BookingConfirmationDocument(BaseModel):

    def __init__(
        self, 
        reservation_id: int, 
        vehicle_id: str, 
        email: bool,
        place_type: str,
        start_at: datetime,
        end_at: datetime,
        price_amount: float,
        payment_id: str,
    ):
        """Initialise les attributs du document de confirmation de réservation."""
        super().__init__()
        self.reservation_id = reservation_id
        self.vehicle_id = vehicle_id
        self.email = email
        self.place_type = place_type
        self.start_at = start_at
        self.end_at = end_at
        self.price_amount = price_amount
        self.payment_id = payment_id

    def generate_pdf(self):
        """Génère un reçu de réservation au format PDF (bytes)."""

        pdf = FPDF(format="A4")
        pdf.set_margins(12, 12, 12)
        pdf.add_page()
    
        # En-tête
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(0, 8, "REÇU DE RÉSERVATION", align="C", new_x="LMARGIN", new_y="NEXT")
    
        pdf.set_font("Helvetica", size=9)
        pdf.cell(
            0, 4, "Confirmation de paiement", align="C", new_x="LMARGIN", new_y="NEXT"
        )
    
        pdf.ln(4)

        line_width = 80
        x_start = (210 - line_width) / 2

        pdf.line(x_start, pdf.get_y(), x_start + line_width, pdf.get_y())
        pdf.ln(6)
    
        # Informations client & réservation
        pdf.set_font("Helvetica", size=9)
    
        fields = [
            ("N° de réservation :", f"#{self.reservation_id}"),
            ("Email client :", self.email),
            ("Véhicule :", self.vehicle_id),
        ]
    
        for label, val in fields:
            pdf.set_font("Helvetica", size=9)
            pdf.cell(38, 5, label, new_x="RIGHT", new_y="LAST")
            pdf.set_font("Helvetica", style="B", size=9)
            pdf.cell(0, 5, val, new_x="LMARGIN", new_y="NEXT")
    
        pdf.ln(4)
    
        # Tableau récapitulatif
        pdf.set_fill_color(240, 243, 246)
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.cell(
            0, 7, "  Détails de la réservation", fill=True, new_x="LMARGIN", new_y="NEXT"
        )
        pdf.ln(2)
    
        pdf.set_font("Helvetica", size=9)
        details = [
            ("Type d'emplacement", self.place_type),
            ("Début", self.start_at.strftime("%d/%m/%Y %H:%M")),
            ("Fin", self.end_at.strftime("%d/%m/%Y %H:%M")),
            ("ID Transaction", self.payment_id),
        ]
    
        for label, val in details:
            pdf.cell(45, 6, label, border="B", new_x="RIGHT", new_y="LAST")
            pdf.cell(0, 6, val, border="B", align="R", new_x="LMARGIN", new_y="NEXT")
    
        pdf.ln(4)
    
        # Total payé
        pdf.set_fill_color(230, 240, 255)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.cell(
            60, 8, " Montant total réglé", fill=True, new_x="RIGHT", new_y="LAST"
        )
        pdf.cell(
            0, 8, f"{self.price_amount} EUR", fill=True, align="R", new_x="LMARGIN", new_y="NEXT"
        )
    
        # Pied de page
        pdf.ln(12)
        pdf.set_font("Helvetica", style="I", size=8)
        pdf.multi_cell(
            0,
            4,
            "Ce document valide votre réservation et sert de preuve de paiement.\nMerci pour votre confiance !",
            align="C",
        )

        self.content = bytes(pdf.output())

        return self.content

    def save(self, storage):
        """Méthode pour sauvegarder le document généré dans le stockage."""
        return storage.save(
            path="booking/confirmations",
            filename=f"{self.reservation_id}.pdf",
            content=self.content
        )

    def from_event(event: Event):
        """Crée une instance de BookingConfirmationDocument à partir d'un événement."""
        return BookingConfirmationDocument(
            reservation_id=event.get("reservation_id"),
            vehicle_id=event.get("vehicle_id"),
            email=event.get("email"),
            place_type=event.get("place_type"),
            start_at=datetime.datetime.fromisoformat(event.get("start_at")),
            end_at=datetime.datetime.fromisoformat(event.get("end_at")),
            price_amount=event.get("price_amount"),
            payment_id=event.get("payment_id")
        )