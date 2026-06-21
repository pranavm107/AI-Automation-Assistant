from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_process_missing_document():
    doc_id = str(uuid4())
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.post(f"/api/v1/documents/{doc_id}/process")
        assert response.status_code == 404
        assert "Document Not Found" in response.json()["message"]

def test_get_content_unprocessed_document():
    doc_id = str(uuid4())
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        mock_doc = MagicMock()
        mock_doc.id = doc_id
        mock_doc.processed = False
        mock_repo.return_value = mock_doc
        response = client.get(f"/api/v1/documents/{doc_id}/content")
        assert response.status_code == 400
        assert "Document Not Processed" in response.json()["message"]

def test_process_valid_document():
    doc_id = str(uuid4())
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        with patch('app.services.document_processing_service.DocumentProcessingService.process_document') as mock_process:
            with patch('app.repositories.document_repository.DocumentRepository.mark_processed') as mock_mark:
                mock_doc = MagicMock()
                mock_doc.id = doc_id
                mock_doc.file_path = "test.pdf"
                mock_repo.return_value = mock_doc
                
                mock_process.return_value = {
                    "text": "test",
                    "character_count": 4,
                    "word_count": 1,
                    "chunk_count": 1,
                    "average_chunk_size": 4,
                    "chunks": ["test"]
                }
                
                response = client.post(f"/api/v1/documents/{doc_id}/process")
                assert response.status_code == 200
                assert response.json()["success"] is True
                assert response.json()["data"]["character_count"] == 4
                mock_mark.assert_called_once_with(doc_id)

def test_get_content_processed_document():
    doc_id = str(uuid4())
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        with patch('app.services.document_processing_service.DocumentProcessingService.process_document') as mock_process:
            mock_doc = MagicMock()
            mock_doc.id = doc_id
            mock_doc.file_path = "test.pdf"
            mock_doc.processed = True
            mock_repo.return_value = mock_doc
            
            mock_process.return_value = {
                "text": "test",
                "character_count": 4,
                "word_count": 1,
                "chunk_count": 1,
                "average_chunk_size": 4,
                "chunks": ["test"]
            }
            
            response = client.get(f"/api/v1/documents/{doc_id}/content")
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert len(response.json()["data"]["chunks"]) == 1
