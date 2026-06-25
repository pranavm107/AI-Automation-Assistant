import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.vector_store_service import VectorStoreService
from app.core.exceptions import AppError

def test_index_document_success():
    mock_repo = MagicMock()
    doc_id = uuid4()
    chunks = ["chunk 1", "chunk 2"]

    with patch('app.services.vector_store_service.FaissManager') as MockFaiss:
        with patch('app.services.vector_store_service.EmbeddingService') as MockEmbedding:
            mock_faiss_instance = MockFaiss.return_value
            mock_faiss_instance.index_exists.return_value = False
            mock_faiss_instance.create_index.return_value = "mock_index"
            mock_faiss_instance.get_vector_count.return_value = 2
            
            mock_embedding_instance = MockEmbedding.return_value
            mock_embedding_instance.generate_embeddings.return_value = [[0.1]*384, [0.2]*384]
            mock_embedding_instance.get_embedding_dimension.return_value = 384
            
            with patch('app.services.vector_store_service.VectorValidationService') as MockValidation:
                service = VectorStoreService(document_repository=mock_repo)
                response = service.index_document(doc_id, chunks)
                
                assert response.success is True
                assert response.data.vector_count == 2
                assert response.data.embedding_dimension == 384
                mock_repo.mark_vector_indexed.assert_called_once()
                mock_faiss_instance.save_index.assert_called_once()

def test_index_document_already_exists():
    mock_repo = MagicMock()
    doc_id = uuid4()
    
    with patch('app.services.vector_store_service.FaissManager') as MockFaiss:
        mock_faiss_instance = MockFaiss.return_value
        mock_faiss_instance.index_exists.return_value = True
        
        service = VectorStoreService(document_repository=mock_repo)
        
        with pytest.raises(AppError) as exc_info:
            service.index_document(doc_id, ["chunk 1"])
        assert exc_info.value.status_code == 400
        assert "Index Already Exists" in str(exc_info.value)

def test_delete_document_index_success():
    mock_repo = MagicMock()
    doc_id = uuid4()
    
    with patch('app.services.vector_store_service.FaissManager') as MockFaiss:
        mock_faiss_instance = MockFaiss.return_value
        mock_faiss_instance.index_exists.return_value = True
        
        service = VectorStoreService(document_repository=mock_repo)
        service.delete_document_index(doc_id)
        
        mock_faiss_instance.delete_index.assert_called_once_with(str(doc_id))
        mock_repo.unmark_vector_indexed.assert_called_once_with(doc_id)
