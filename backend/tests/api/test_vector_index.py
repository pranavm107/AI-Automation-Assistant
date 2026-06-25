from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_create_vector_index_success():
    doc_id = str(uuid4())
    
    with patch('app.api.v1.vector_index.DocumentService') as MockDocService:
        mock_doc_service = MockDocService.return_value
        mock_content = MagicMock()
        mock_content.data.chunks = ["chunk1"]
        mock_doc_service.get_document_content.return_value = mock_content
        
        with patch('app.api.v1.vector_index.VectorStoreService') as MockVectorStore:
            mock_vector_store = MockVectorStore.return_value
            mock_response = MagicMock()
            mock_response.success = True
            mock_response.model_dump.return_value = {
                "success": True,
                "message": "Document indexed successfully",
                "data": {
                    "document_id": doc_id,
                    "faiss_document_id": doc_id,
                    "vector_count": 1,
                    "embedding_dimension": 384,
                    "index_type": "IndexFlatL2"
                }
            }
            # We must configure the mock to return a dictionary or a pydantic model that FastAPI can serialize
            mock_vector_store.index_document.return_value = mock_response.model_dump()
            
            response = client.post(f"/api/v1/documents/{doc_id}/index")
            
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["data"]["vector_count"] == 1

def test_get_vector_index_status():
    doc_id = str(uuid4())
    
    with patch('app.api.v1.vector_index.VectorStoreService') as MockVectorStore:
        mock_vector_store = MockVectorStore.return_value
        mock_vector_store.get_index_status.return_value = {
            "success": True,
            "data": {
                "vector_indexed": True,
                "vector_count": 10,
                "faiss_document_id": doc_id,
                "indexed_at": "2023-10-10T00:00:00"
            }
        }
        
        response = client.get(f"/api/v1/documents/{doc_id}/index/status")
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["vector_indexed"] is True
