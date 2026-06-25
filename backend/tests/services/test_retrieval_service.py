import pytest
from unittest.mock import MagicMock, patch
from app.services.retrieval_service import RetrievalService
from app.core.exceptions import AppError

def test_calculate_similarity():
    service = RetrievalService()
    assert service.calculate_similarity(0.0) == 1.0
    assert service.calculate_similarity(1.0) == 0.5
    assert service.calculate_similarity(-1.0) == 0.0

def test_search_document_success():
    with patch('app.services.retrieval_service.EmbeddingService') as MockEmbedding:
        with patch('app.services.retrieval_service.FaissManager') as MockFaiss:
            mock_embedding = MockEmbedding.return_value
            mock_embedding.generate_embeddings.return_value = [[0.1, 0.2]]
            
            mock_faiss = MockFaiss.return_value
            mock_faiss.index_exists.return_value = True
            
            mock_index = MagicMock()
            mock_index.search.return_value = ([[0.5, 1.2]], [[0, 1]])
            mock_faiss.load_index.return_value = mock_index
            mock_faiss.load_chunk_metadata.return_value = ["chunk 0", "chunk 1"]
            
            service = RetrievalService()
            results = service.search_document("doc123", "query", top_k=2)
            
            assert len(results) == 2
            # Results should be sorted by score descending (so distance ascending)
            assert results[0]['chunk'] == "chunk 0"
            assert results[0]['score'] > results[1]['score']

def test_search_document_missing_index():
    with patch('app.services.retrieval_service.FaissManager') as MockFaiss:
        mock_faiss = MockFaiss.return_value
        mock_faiss.index_exists.return_value = False
        
        service = RetrievalService()
        with pytest.raises(AppError) as exc_info:
            service.search_document("doc123", "query")
        assert exc_info.value.status_code == 404
