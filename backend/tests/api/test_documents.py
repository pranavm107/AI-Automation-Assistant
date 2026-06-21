from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_upload_valid_document():
    with patch('app.services.upload_service.UploadService.upload_file') as mock_upload:
        with patch('app.repositories.document_repository.DocumentRepository.create') as mock_repo:
            import asyncio
            async def mock_upload_async(*args, **kwargs):
                return ("safe_name.pdf", "test.pdf", 1000, "pdf")
            mock_upload.side_effect = mock_upload_async
            
            mock_doc = MagicMock()
            mock_doc.id = uuid4()
            mock_repo.return_value = mock_doc
            
            response = client.post(
                "/api/v1/documents/upload", 
                files={"file": ("test.pdf", b"test content", "application/pdf")}
            )
            assert response.status_code == 200
            assert response.json()["success"] is True

def test_upload_invalid_file_type():
    response = client.post(
        "/api/v1/documents/upload", 
        files={"file": ("test.exe", b"test content", "application/x-msdownload")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["message"]

def test_get_documents():
    with patch('app.repositories.document_repository.DocumentRepository.get_all') as mock_repo:
        mock_repo.return_value = []
        response = client.get("/api/v1/documents")
        assert response.status_code == 200
        assert response.json()["success"] is True

def test_get_document_not_found():
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        mock_repo.return_value = None
        doc_id = str(uuid4())
        response = client.get(f"/api/v1/documents/{doc_id}")
        assert response.status_code == 404

def test_delete_document_not_found():
    with patch('app.repositories.document_repository.DocumentRepository.get_by_id') as mock_repo:
        mock_repo.return_value = None
        doc_id = str(uuid4())
        response = client.delete(f"/api/v1/documents/{doc_id}")
        assert response.status_code == 404
