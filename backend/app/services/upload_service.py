import os
import uuid
from typing import Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import AppError
import logging

logger = logging.getLogger(__name__)

class UploadService:
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

    def __init__(self):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    async def upload_file(self, file: UploadFile) -> Tuple[str, str, int, str]:
        if not file.filename:
            raise AppError("Filename is missing.", status_code=400)

        _, ext = os.path.splitext(file.filename.lower())
        if ext not in self.ALLOWED_EXTENSIONS:
            raise AppError(f"Unsupported file type. Supported types: {', '.join(self.ALLOWED_EXTENSIONS)}", status_code=400)
        
        file_type = ext[1:]
        safe_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

        size = 0
        try:
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > settings.MAX_UPLOAD_SIZE:
                        f.close()
                        os.remove(file_path)
                        raise AppError(f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE} bytes.", status_code=400)
                    f.write(chunk)
        except AppError:
            raise
        except Exception as e:
            logger.error(f"Failed to save file: {e}", exc_info=True)
            if os.path.exists(file_path):
                os.remove(file_path)
            raise AppError("Storage Failure: Failed to save the file.", status_code=500)

        return safe_filename, file.filename, size, file_type

    def delete_file(self, filename: str) -> None:
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Deleted file {file_path}")
            except Exception as e:
                logger.error(f"Failed to delete file {file_path}: {e}")
