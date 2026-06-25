import logging
import math
from typing import List, Dict, Any
from app.core.exceptions import AppError
from app.services.embedding_service import EmbeddingService
from app.vector_store.faiss_manager import FaissManager
import numpy as np

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.faiss_manager = FaissManager()

    def calculate_similarity(self, l2_distance: float) -> float:
        """
        Normalizes an L2 distance into a confidence score between 0.0 and 1.0.
        For L2 distance, smaller is better.
        """
        if l2_distance < 0:
            return 0.0
        # Simple normalization: 1 / (1 + distance). 
        # Distance 0 => Score 1.0
        # Distance -> infinity => Score -> 0.0
        return 1.0 / (1.0 + float(l2_distance))

    def search_document(self, document_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches a single document's FAISS index for the most relevant chunks.
        
        Returns:
            List of dictionaries containing:
            - 'chunk': The string text of the chunk
            - 'chunk_id': The index position of the chunk
            - 'score': The normalized confidence score (0.0 to 1.0)
            - 'distance': The raw L2 distance
        """
        logger.info(f"Retrieving top {top_k} chunks for document {document_id}")
        
        # Ensure the index and metadata exist
        if not self.faiss_manager.index_exists(document_id):
            raise AppError(f"FAISS index missing for document {document_id}", status_code=404)
            
        # Load FAISS index and chunk metadata
        index = self.faiss_manager.load_index(document_id)
        chunks = self.faiss_manager.load_chunk_metadata(document_id)
        
        # Determine actual K
        actual_k = min(top_k, len(chunks))
        if actual_k == 0:
            raise AppError(f"No chunks found for document {document_id}", status_code=404)
            
        # Generate embedding for the query
        query_embeddings = self.embedding_service.generate_embeddings([query])
        query_vector = np.array(query_embeddings, dtype=np.float32)
        
        # Search FAISS
        try:
            distances, indices = index.search(query_vector, actual_k)
        except Exception as e:
            logger.error(f"FAISS search failed: {e}", exc_info=True)
            raise AppError(f"Retrieval Failure: {str(e)}", status_code=500)
            
        # Map results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            # FAISS might return -1 for indices if not enough vectors are found
            if idx == -1:
                continue
                
            chunk_text = chunks[idx] if idx < len(chunks) else ""
            score = self.calculate_similarity(dist)
            
            results.append({
                "chunk": chunk_text,
                "chunk_id": int(idx),
                "score": score,
                "distance": float(dist),
                "document_id": document_id
            })
            
        # Sort by score descending (highest confidence first)
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def search_top_k(self, document_ids: List[str], query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches across multiple documents and returns the top K chunks globally.
        """
        logger.info(f"Retrieving globally across {len(document_ids)} documents.")
        
        all_results = []
        for doc_id in document_ids:
            try:
                # We pull top_k from EACH document, then we will sort all of them together
                doc_results = self.search_document(doc_id, query, top_k)
                all_results.extend(doc_results)
            except AppError as e:
                logger.warning(f"Skipping document {doc_id} during global search: {str(e)}")
            except Exception as e:
                logger.error(f"Error searching document {doc_id}: {str(e)}", exc_info=True)
                
        # Sort all aggregated results by score descending
        all_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Return only the top K globally
        return all_results[:top_k]
