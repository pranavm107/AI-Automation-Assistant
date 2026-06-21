import logging
from typing import List
from app.core.exceptions import ChunkingError

logger = logging.getLogger(__name__)

class ChunkingService:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        if not text:
            return []

        try:
            chunks = []
            start = 0
            text_length = len(text)

            while start < text_length:
                end = start + self.chunk_size
                
                if end < text_length:
                    last_newline = text.rfind('\n', start, end)
                    last_space = text.rfind(' ', start, end)
                    
                    if last_newline != -1 and (end - last_newline) < 150:
                        end = last_newline + 1
                    elif last_space != -1 and (end - last_space) < 50:
                        end = last_space + 1

                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)

                next_start = end - self.overlap
                # Prevent infinite loop if we didn't advance
                if next_start <= start:
                    start = end
                else:
                    start = next_start

            return chunks
        except Exception as e:
            logger.error(f"Failed to chunk text: {e}", exc_info=True)
            raise ChunkingError("Failed to chunk the provided text.")
