import os
import logging
from pypdf import PdfReader
from app.core.exceptions import PDFExtractionError

logger = logging.getLogger(__name__)

class PDFService:
    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise PDFExtractionError("PDF file missing or path is invalid.")

        try:
            reader = PdfReader(file_path)
            extracted_text = []

            if len(reader.pages) == 0:
                raise PDFExtractionError("PDF document is empty.")

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

            full_text = "\n".join(extracted_text).strip()
            
            if not full_text:
                raise PDFExtractionError("No extractable text found in the PDF.")
                
            return full_text
            
        except PDFExtractionError:
            raise
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}", exc_info=True)
            raise PDFExtractionError("Failed to parse or extract text from the PDF file. The file may be corrupted.")
