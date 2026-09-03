import pika

class Consumer:


    # Initialize the consumer with RabbitMQ connection parameters
    def __init__(self, amqp_url: str):
        params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()


    # Setup the exchange, queue, and routing keys for the consumer
    def setup(self, exchange_name: str, queue_name: str, routing_keys: list, on_message_callback):
        # Configure the exchange and queue
        self.channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True, passive=True)
        self.channel.queue_declare(queue=queue_name, durable=True)

        # Subscribe to the specified routing keys
        for routing_key in routing_keys:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

        self.on_message_callback = on_message_callback
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_message)


    # Callback function to handle incoming messages
    def on_message(self, ch, method, properties, body):
        try:
            self.on_message_callback(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"[ERREUR] Traitment error : {e}")
            # In case of error, do not requeue the faulty message (requeue=False)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


    # Start consuming messages from the queue
    def start_consuming(self):
        print("[*] Worker listening for messages !")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.__del__()


    # Close the connection and channel when the consumer is deleted
    def __del__(self):
        self.channel.stop_consuming()
        self.connection.close()