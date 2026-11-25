import json

class Event:

    def __init__(self, channel, method, properties, body):
        """Initializes the Event object with the provided channel, method, properties, and body."""
        self.channel = channel
        self.method = method
        self.properties = properties
        self.data = json.loads(body)

    def get(self, key: str, default=None):
        """Get the value associated with a specific key from the event data."""
        return self.data.get(key, default)

    def toString(self):
        """Returns a string representation of the event data."""
        return json.dumps(self.data)