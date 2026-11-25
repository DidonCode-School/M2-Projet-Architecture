import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    # RabbitMQ configuration
    AMQP_URL = os.environ.get("CLOUDAMQP_URL", "amqps://user:password@hostname/vhost")
    EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME", "event-bus")
    QUEUE_NAME = os.environ.get("QUEUE_NAME", "messages-service-queue")

    # Logging configuration
    LOGGER_NAME = os.environ.get("LOGGER_NAME", "MonProjet")

    LOG_LEVEL = os.environ.get("LOGGER_LEVEL", "INFO")
    LOG_DIR = os.environ.get("LOG_DIR", "logs")
    LOG_FILE = os.environ.get("LOG_FILE", "app.log")
    LOG_FORMAT = os.environ.get("LOG_FORMAT", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    DATE_FORMAT = os.environ.get("DATE_FORMAT", "%d/%m/%Y %H:%M:%S")

    # API
    API_HOST = os.environ.get("API_HOST", "localhost")
    API_PORT = int(os.environ.get("API_PORT", 8000))

    # Services
    VEHICLE_SERVICE_URL = os.environ.get("VEHICLE_SERVICE_URL", "http://localhost:8000")
