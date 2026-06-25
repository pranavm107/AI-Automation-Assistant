import os
import faiss
import numpy as np
import logging
import json
from typing import List, Optional
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

class FaissManager:
    def __init__(self, base_dir: str = "vector_store"):
        self.indexes_dir = os.path.join(base_dir, "indexes")
        self.metadata_dir = os.path.join(base_dir, "metadata")
        os.makedirs(self.indexes_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)

    def _get_index_path(self, document_id: str) -> str:
        return os.path.join(self.indexes_dir, f"{document_id}.index")

    def create_index(self, dimension: int, embeddings: List[List[float]]) -> faiss.IndexFlatL2:
        """Creates a new IndexFlatL2 FAISS index and populates it with embeddings."""
        logger.info(f"Creating FAISS IndexFlatL2 with dimension {dimension} for {len(embeddings)} vectors.")
        try:
            index = faiss.IndexFlatL2(dimension)
            # FAISS requires numpy arrays of type float32
            vectors_np = np.array(embeddings, dtype=np.float32)
            index.add(vectors_np)
            return index
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {e}", exc_info=True)
            raise AppError(f"FAISS Creation Failure: {str(e)}", status_code=500)

    def save_index(self, index: faiss.IndexFlatL2, document_id: str) -> str:
        """Saves a FAISS index to disk."""
        path = self._get_index_path(document_id)
        logger.info(f"Saving FAISS index to {path}")
        try:
            faiss.write_index(index, path)
            return path
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}", exc_info=True)
            raise AppError(f"FAISS Save Failure: {str(e)}", status_code=500)

    def load_index(self, document_id: str) -> faiss.Index:
        """Loads a FAISS index from disk."""
        path = self._get_index_path(document_id)
        if not os.path.exists(path):
            raise AppError(f"Index Missing: No index found for document {document_id}", status_code=404)
            
        logger.info(f"Loading FAISS index from {path}")
        try:
            return faiss.read_index(path)
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {e}", exc_info=True)
            raise AppError(f"FAISS Load Failure: {str(e)}", status_code=500)

    def delete_index(self, document_id: str) -> bool:
        """Deletes a FAISS index file from disk."""
        path = self._get_index_path(document_id)
        if os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted FAISS index at {path}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete FAISS index: {e}", exc_info=True)
                raise AppError(f"FAISS Delete Failure: {str(e)}", status_code=500)
        return False

    def get_vector_count(self, index: faiss.Index) -> int:
        """Returns the number of vectors in an index."""
        return index.ntotal

    def index_exists(self, document_id: str) -> bool:
        """Checks if a FAISS index exists for a given document."""
        return os.path.exists(self._get_index_path(document_id))

    def _get_metadata_path(self, document_id: str) -> str:
        return os.path.join(self.metadata_dir, f"{document_id}.json")

    def save_chunk_metadata(self, document_id: str, chunks: List[str]) -> str:
        """Saves chunks as JSON metadata mapped to the FAISS index."""
        path = self._get_metadata_path(document_id)
        logger.info(f"Saving chunk metadata to {path}")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"document_id": document_id, "chunks": chunks}, f)
            return path
        except Exception as e:
            logger.error(f"Failed to save chunk metadata: {e}", exc_info=True)
            raise AppError(f"Metadata Save Failure: {str(e)}", status_code=500)

    def load_chunk_metadata(self, document_id: str) -> List[str]:
        """Loads chunk metadata from disk."""
        path = self._get_metadata_path(document_id)
        if not os.path.exists(path):
            raise AppError(f"Metadata Missing: No metadata found for document {document_id}", status_code=404)
        
        logger.info(f"Loading chunk metadata from {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("chunks", [])
        except Exception as e:
            logger.error(f"Failed to load chunk metadata: {e}", exc_info=True)
            raise AppError(f"Metadata Load Failure: {str(e)}", status_code=500)

    def delete_chunk_metadata(self, document_id: str) -> bool:
        """Deletes chunk metadata from disk."""
        path = self._get_metadata_path(document_id)
        if os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted chunk metadata at {path}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete chunk metadata: {e}", exc_info=True)
                raise AppError(f"Metadata Delete Failure: {str(e)}", status_code=500)
        return False
