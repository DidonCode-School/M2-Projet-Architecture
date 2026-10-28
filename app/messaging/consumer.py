from app.messaging.event import Event 
import pika

class Consumer:

    def __init__(self, amqp_url: str):
        """Initialize the consumer with RabbitMQ connection parameters."""
        params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.is_running = False


    def setup(self, exchange_name: str, queue_name: str, routing_keys: list, on_event_callback):
        """Setup the exchange, queue, and routing keys for the consumer."""
        # Configure the exchange and queue
        self.channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True, passive=True)
        self.channel.queue_declare(queue=queue_name, durable=True)

        # Subscribe to the specified routing keys
        for routing_key in routing_keys:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

        self.on_event_callback = on_event_callback
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_message)

    def on_message(self, channel, method, properties, body):
        """Callback function to handle incoming messages from the queue."""
        try:
            # Create an Event object and invoke the callback function
            self.on_event_callback(Event(channel, method, properties, body))
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"[ERREUR] Traitment error : {e}")
            # In case of error, do not requeue the faulty message (requeue=False)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        """Start consuming messages from the queue."""
        if(self.is_running):
            print("[INFO] Consumer is already running.")
            return

        self.is_running = True
        self.channel.start_consuming()

    def stop_consuming(self):
        """Closes the consumer connection and stops consuming messages."""
        if not self.is_running:
            print("[INFO] Consumer is not running.")
            return

        self.channel.stop_consuming()
        self.connection.close()
        self.is_running = False