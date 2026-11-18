from app.core.logger import load_logger
from app.worker import Worker

logger = load_logger()

worker = Worker()
worker.start()