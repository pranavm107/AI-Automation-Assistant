import os
import re
import logging
from app.core.exceptions import TXTExtractionError

logger = logging.getLogger(__name__)

class TextService:
    def extract_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise TXTExtractionError("TXT file missing or path is invalid.")

        try:
            # Try utf-8 first, fallback to latin-1
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    full_text = f.read()
            except UnicodeDecodeError:
                logger.warning(f"UTF-8 decoding failed for {file_path}, falling back to latin-1")
                with open(file_path, "r", encoding="latin-1") as f:
                    full_text = f.read()
            
            if not full_text.strip():
                raise TXTExtractionError("No extractable text found in the TXT document.")
                
            return full_text
            
        except TXTExtractionError:
            raise
        except Exception as e:
            logger.error(f"Failed to extract text from TXT: {e}", exc_info=True)
            raise TXTExtractionError("Failed to read the TXT file.")

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
            
        text = text.replace('\r', '')
        text = re.sub(r'\t+', ' ', text)
        
        # Remove extra whitespace inside lines (but keep newlines)
        cleaned_lines = []
        for line in text.split('\n'):
            line = re.sub(r'[ \t]+', ' ', line).strip()
            if line:
                cleaned_lines.append(line)
                
        cleaned_text = '\n'.join(cleaned_lines)
        return cleaned_text
