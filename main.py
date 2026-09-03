import json
import os
from app.consumer import Consumer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get RabbitMQ connection parameters from environment variables
AMQP_URL = os.environ.get("CLOUDAMQP_URL", "amqps://user:password@hostname/vhost")
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME", "event-bus")
QUEUE_NAME = os.environ.get("QUEUE_NAME", "messages-service-queue")

# Callback function to handle incoming messages
def on_message(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[EVENT RECEIVED] Routing key: '{method.routing_key}'")
    print(f"MMessage content: {data}")

# Define the consumer and start consuming messages
event_bus_consumer = Consumer(AMQP_URL)
event_bus_consumer.setup(
    exchange_name=EXCHANGE_NAME,
    queue_name=QUEUE_NAME,
    routing_keys=[
        "access.entry",
        "access.exit",
        "reservation.confirmation"
    ],
    on_message_callback=on_message
)
event_bus_consumer.start_consuming()