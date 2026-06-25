import os
import logging
from typing import Dict, Any
from app.core.exceptions import AppError
from app.services.pdf_service import PDFService
from app.services.docx_service import DOCXService
from app.services.text_service import TextService
from app.services.chunking_service import ChunkingService

logger = logging.getLogger(__name__)

class DocumentProcessingService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.docx_service = DOCXService()
        self.text_service = TextService()
        self.chunking_service = ChunkingService()

    def process_document(self, file_path: str) -> Dict[str, Any]:
        logger.info(f"Document Processing Started for: {file_path}")
        
        if not os.path.exists(file_path):
            raise AppError("File missing or path is invalid.", status_code=404)

        _, ext = os.path.splitext(file_path.lower())
        logger.info(f"File Type Detected: {ext}")

        try:
            if ext == '.pdf':
                raw_text = self.pdf_service.extract_text(file_path)
            elif ext == '.docx':
                raw_text = self.docx_service.extract_text(file_path)
            elif ext == '.txt':
                raw_text = self.text_service.extract_text(file_path)
            else:
                raise AppError(f"Unsupported File Type: {ext}", status_code=400)
                
            logger.info("Extraction Success")
        except AppError:
            raise
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise AppError("Extraction failed due to an unexpected error.", status_code=500)

        try:
            cleaned_text = self.text_service.clean_text(raw_text)
            logger.info("Cleaning Success")
        except Exception as e:
            logger.error(f"Cleaning failed: {e}")
            raise AppError("Failed to clean the extracted text.", status_code=500)

        try:
            chunks = self.chunking_service.chunk_text(cleaned_text)
            logger.info(f"Chunking Success. Generated {len(chunks)} chunks.")
        except AppError:
            raise
        except Exception as e:
            logger.error(f"Chunking failed: {e}")
            raise AppError("Failed to generate text chunks.", status_code=500)

        character_count = len(cleaned_text)
        word_count = len(cleaned_text.split())
        chunk_count = len(chunks)
        average_chunk_size = sum(len(c) for c in chunks) / chunk_count if chunk_count > 0 else 0

        logger.info("Processing Complete")

        return {
            "text": cleaned_text,
            "character_count": character_count,
            "word_count": word_count,
            "chunk_count": chunk_count,
            "average_chunk_size": int(average_chunk_size),
            "chunks": chunks
        }
