from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_generate_embeddings_success():
    doc_id = str(uuid4())
    
    with patch('app.services.document_service.DocumentService.get_document_content') as mock_get_content:
        with patch('app.services.embedding_service.EmbeddingService.generate_embeddings') as mock_generate:
            with patch('app.repositories.document_repository.DocumentRepository.mark_embeddings_generated') as mock_mark:
                
                # Mock content return
                mock_content_response = MagicMock()
                mock_content_response.data.chunks = ["chunk1", "chunk2"]
                mock_get_content.return_value = mock_content_response
                
                # Mock embeddings return
                mock_generate.return_value = [[0.1]*384, [0.2]*384]
                
                response = client.post(f"/api/v1/documents/{doc_id}/embeddings")
                
                assert response.status_code == 200
                assert response.json()["success"] is True
                assert response.json()["data"]["chunk_count"] == 2
                assert response.json()["data"]["vector_count"] == 2
                assert response.json()["data"]["embedding_dimension"] == 384
                
                mock_mark.assert_called_once()

def test_get_embedding_status():
    doc_id = str(uuid4())
    
    with patch('app.services.document_service.DocumentService.get_document_by_id') as mock_get_doc:
        mock_doc = MagicMock()
        mock_doc.embeddings_generated = True
        mock_doc.embedding_model = "all-MiniLM-L6-v2"
        mock_doc.embedding_dimension = 384
        mock_doc.embeddings_generated_at = None
        mock_get_doc.return_value = mock_doc
        
        response = client.get(f"/api/v1/documents/{doc_id}/embeddings/status")
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["embeddings_generated"] is True
        assert response.json()["data"]["embedding_model"] == "all-MiniLM-L6-v2"
