from dotenv import load_dotenv
import os
from app.models.access.access_entry import AccessEntryDocument
from app.models.access.access_exit import AccessExitDocument
from app.models.booking.booking_confirmation import BookingConfirmationDocument

load_dotenv()

class Config:

    AMQP_URL = os.environ.get("CLOUDAMQP_URL", "amqps://user:password@hostname/vhost")
    EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME", "event-bus")
    QUEUE_NAME = os.environ.get("QUEUE_NAME", "messages-service-queue")

    ROUTING_KEYS = {
        "access.entry": AccessEntryDocument,
        "access.exit": AccessExitDocument,
        "booking.confirmed": BookingConfirmationDocument
    }