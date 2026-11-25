import signal
import threading
from app.core.logger import load_logger
from app.api.api import Api
from app.messaging.worker import Worker
import threading

load_logger()

def main():
    shutdown_event = threading.Event()

    def on_signal(_signum: int, _frame: object) -> None:
        shutdown_event.set()

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    api = Api()
    worker = Worker()

    api.start()
    worker.start()

    try:
        while not shutdown_event.is_set() and api.is_alive() and worker.is_alive():
            shutdown_event.wait(timeout=1.0)
    finally:
        worker.stop()
        api.stop()

if __name__ == "__main__":
    main()