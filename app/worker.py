from app.messaging.event import Event
from app.messaging.consumer import Consumer
from app.core.config import Config
from app.storage.storage import Storage

class Worker:

    def __init__(self):
        """Initializes the Worker class, sets up the storage and consumer for processing messages from the event bus."""

        # Define the storage path for saving generated documents
        self.storage = Storage()

        # Define the consumer and start consuming messages
        self.consumer = Consumer(Config.AMQP_URL)
        self.consumer.setup(
            exchange_name=Config.EXCHANGE_NAME,
            queue_name=Config.QUEUE_NAME,
            routing_keys=Config.ROUTING_KEYS.keys(),
            on_event_callback=self.on_message
        )

    def on_message(self, event: Event):
        """Callback function to handle incoming messages from the event bus."""
        print(f"[INFO] Received message with routing key: {event.method.routing_key}")

        routing_key = event.method.routing_key

        try:
            document_template = Config.ROUTING_KEYS[routing_key]

            if document_template == None:
                print(f"[INFO] No document template found for routing key: {routing_key}")
                return

            pdf = document_template.from_event(event)
            pdf.generate_pdf()
            pdf.save(self.storage)
        except Exception as e:
            print(f"[ERREUR] Impossible de traiter le message : {e}")

    def start(self):
        """Starts the worker to listen for messages from the event bus."""
        print("[*] Worker listening for messages !")
        try:
            self.consumer.start_consuming()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        """Stops the worker and closes the consumer connection."""
        print("[*] Stopping worker...")
        self.consumer.stop_consuming()
        print("[*] Worker stopped.")
