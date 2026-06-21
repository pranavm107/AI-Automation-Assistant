import os
import logging
from docx import Document
from app.core.exceptions import DOCXExtractionError

logger = logging.getLogger(__name__)

class DOCXService:
    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise DOCXExtractionError("DOCX file missing or path is invalid.")

        try:
            doc = Document(file_path)
            paragraphs = []

            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append(text)

            full_text = "\n".join(paragraphs).strip()
            
            if not full_text:
                raise DOCXExtractionError("No extractable text found in the DOCX document.")
                
            return full_text

        except DOCXExtractionError:
            raise
        except Exception as e:
            logger.error(f"Failed to extract text from DOCX: {e}", exc_info=True)
            raise DOCXExtractionError("Failed to parse or extract text from the DOCX file. The file may be corrupted.")
