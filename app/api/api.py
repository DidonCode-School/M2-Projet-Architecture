import threading
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from app.core.config import Config
import uvicorn

class Api(threading.Thread):
    def __init__(self):
        super().__init__(name="api-thread", daemon=True)

        self.app = FastAPI()
        self.setup_routes()
        self.config = uvicorn.Config(
            app=self.app,
            host=Config.API_HOST,
            port=Config.API_PORT,
            log_level=Config.LOG_LEVEL,
        )

    def setup_routes(self):
        self.app.add_api_route("/health", self.health, methods=["GET"])
        self.app.add_api_route("/metrics", self.metrics, methods=["GET"])

    def health(self):
        """Health check endpoint to verify the service is running."""
        return {"status": "ok"}

    def metrics(self):
        """Metrics endpoint to expose Prometheus metrics."""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    def run(self):
        """Run the FastAPI application using Uvicorn."""
        self.server = uvicorn.Server(self.config)
        self.server.run()

    async def stop(self, timeout: float = 5.0):
        """Stop the FastAPI application."""
        await self.server.shutdown()
        await self.join(timeout=timeout)