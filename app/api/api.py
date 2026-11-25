import threading
from app.storage.storage import Storage
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from app.core.config import Config
import uvicorn

class Api(threading.Thread):
    def __init__(self):
        super().__init__(name="api-thread", daemon=True)
        self.storage = Storage()
        self.app = FastAPI()
        self.setup_routes()
        self.config = uvicorn.Config(
            app=self.app,
            host=Config.API_HOST,
            port=Config.API_PORT,
            log_level=Config.LOG_LEVEL,
        )
        

    def setup_routes(self):
        self.app.add_api_route("/v1/health", self.health, methods=["GET"])
        self.app.add_api_route("/v1/metrics", self.metrics, methods=["GET"])
        self.app.add_api_route(
            "/v1/documents/access/entrys/{uuid}",
            self.get_access_entry_pdf,
            methods=["GET"],
        )
        self.app.add_api_route(
            "/v1/documents/access/exits/{uuid}",
            self.get_access_exit_pdf,
            methods=["GET"],
        )
        self.app.add_api_route(
            "/v1/documents/booking/confirmations/{uuid}",
            self.get_booking_confirmation_pdf,
            methods=["GET"],
        )

    def health(self):
        """Health check endpoint to verify the service is running."""
        return {"status": "ok"}

    def metrics(self):
        """Metrics endpoint to expose Prometheus metrics."""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    def get_access_entry_pdf(self, uuid: str):
        """Return a stored Access Entry PDF file."""
        return self.get_pdf("access/entrys", uuid)

    def get_access_exit_pdf(self, uuid: str):
        """Return a stored Access Exit PDF file."""
        return self.get_pdf("access/exits", uuid)

    def get_booking_confirmation_pdf(self, uuid: str):
        """Return a stored Booking Confirmation PDF file."""
        return self.get_pdf("booking/confirmations", uuid)

    def get_pdf(self, sub_path: str, uuid: str):
        """Return a stored PDF file."""
        filename = f"{uuid}.pdf"
        file_path = self.storage.resolve_file_path(sub_path, filename)

        if file_path is None:
            raise HTTPException(status_code=400, detail="Invalid document identifier")

        if not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename,
        )

    def run(self):
        """Run the FastAPI application using Uvicorn."""
        self.server = uvicorn.Server(self.config)
        self.server.run()

    async def stop(self, timeout: float = 5.0):
        """Stop the FastAPI application."""
        await self.server.shutdown()
        await self.join(timeout=timeout)