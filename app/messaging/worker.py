import logging
import threading
from app.messaging.event import Event
from app.messaging.consumer import Consumer
from app.core.config import Config
from app.storage.storage import Storage
from app.models.access.access_entry import AccessEntryDocument
from app.models.access.access_exit import AccessExitDocument
from app.models.booking.booking_confirmation import BookingConfirmationDocument

ROUTING_KEYS = {
    "access.entry": AccessEntryDocument,
    "access.exit": AccessExitDocument,
    "booking.confirmed": BookingConfirmationDocument
}

class Worker(threading.Thread):

    def __init__(self):
        """Initializes the Worker class, sets up the storage and consumer for processing messages from the event bus."""
        super().__init__(name="worker-thread", daemon=True)
        
        self.logger = logging.getLogger(Config.LOGGER_NAME)

        # Define the storage path for saving generated documents
        self.storage = Storage()

        # Define the consumer and start consuming messages
        self.consumer = Consumer(Config.AMQP_URL)
        self.consumer.setup(
            exchange_name=Config.EXCHANGE_NAME,
            queue_name=Config.QUEUE_NAME,
            routing_keys=ROUTING_KEYS.keys(),
            on_event_callback=self.on_message
        )

    def on_message(self, event: Event):
        """Callback function to handle incoming messages from the event bus."""
        self.logger.info(
            f"Received message with routing key: {event.method.routing_key}; {event.toString()}"
        )

        routing_key = event.method.routing_key

        try:
            document_template = ROUTING_KEYS[routing_key]

            if document_template == None:
                self.logger.info(
                    f"No document template found for routing key: {routing_key}"
                )
                return

            pdf = document_template.from_event(event)
            pdf.generate_pdf()
            pdf.save(self.storage)
        except Exception as e:
            self.logger.error(f"Impossible de traiter le message : {e}")

    def run(self):
        """Starts the worker to listen for messages from the event bus."""
        self.logger.info("[*] Worker listening for messages !")
        self.consumer.start_consuming()

    def stop(self, timeout: float = 5.0):
        """Stops the worker and closes the consumer connection."""
        self.logger.info("Stopping worker...")
        self.consumer.stop_consuming()
        if self.is_alive():
            self.join(timeout=timeout)
        self.logger.info("Worker stopped.")
