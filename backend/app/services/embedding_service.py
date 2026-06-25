import logging
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

class EmbeddingService:
    _instance = None
    _model: Optional[SentenceTransformer] = None
    _model_name: str = 'all-MiniLM-L6-v2'
    _dimension: int = 384

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def load_model(self) -> None:
        """Lazy loads the SentenceTransformer model to prevent memory bloat."""
        if self._model is None:
            logger.info(f"Loading embedding model: {self._model_name}")
            try:
                self._model = SentenceTransformer(self._model_name)
                logger.info(f"Model {self._model_name} loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}", exc_info=True)
                raise AppError(f"Model Load Failure: {str(e)}", status_code=500)

    def generate_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text chunks."""
        if not chunks:
            raise AppError("Empty Chunks provided for embedding generation.", status_code=400)
            
        self.load_model()
        
        logger.info(f"Generating embeddings for {len(chunks)} chunks.")
        try:
            # Generate embeddings and convert from numpy arrays to lists of floats
            embeddings = self._model.encode(chunks)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}", exc_info=True)
            raise AppError(f"Embedding Generation Failure: {str(e)}", status_code=500)

    def get_embedding_dimension(self) -> int:
        """Returns the expected dimension of the embeddings."""
        return self._dimension

    def get_model_name(self) -> str:
        """Returns the name of the loaded model."""
        return self._model_name
