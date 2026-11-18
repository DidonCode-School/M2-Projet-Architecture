import os
from dotenv import load_dotenv
from app.models.access.access_entry import AccessEntryDocument
from app.models.access.access_exit import AccessExitDocument
from app.models.booking.booking_confirmation import BookingConfirmationDocument

# Load environment variables from .env file
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

    LOGGER_NAME = os.environ.get("LOGGER_NAME", "MonProjet")

    LOG_LEVEL = os.environ.get("LOGGER_LEVEL", "INFO")
    LOG_DIR = os.environ.get("LOG_DIR", "logs")
    LOG_FILE = os.environ.get("LOG_FILE", "app.log")
    LOG_FORMAT = os.environ.get("LOG_FORMAT", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    DATE_FORMAT = os.environ.get("DATE_FORMAT", "%d/%m/%Y %H:%M:%S")
