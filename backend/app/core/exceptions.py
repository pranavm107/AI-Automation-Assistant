from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.error(f"AppError: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message, "errors": []}
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "An unexpected error occurred.", "errors": []}
        )

class PDFExtractionError(AppError):
    def __init__(self, message: str = "Failed to extract text from PDF"):
        super().__init__(message, status_code=400)

class DOCXExtractionError(AppError):
    def __init__(self, message: str = "Failed to extract text from DOCX"):
        super().__init__(message, status_code=400)

class TXTExtractionError(AppError):
    def __init__(self, message: str = "Failed to extract text from TXT"):
        super().__init__(message, status_code=400)

class ChunkingError(AppError):
    def __init__(self, message: str = "Failed to chunk text"):
        super().__init__(message, status_code=500)
