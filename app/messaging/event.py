import json

class Event:

    # Initialize the Event object with channel, method, properties, and body
    def __init__(self, channel, method, properties, body):
        self.channel = channel
        self.method = method
        self.properties = properties
        self.data = json.loads(body)

    # Get the value associated with a specific key from the event data
    def get(self, key: str, default=None):
        return self.data.get(key, default)