from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_ask_document_api_success():
    doc_id = str(uuid4())
    
    with patch('app.api.v1.rag.RagService') as MockRag:
        mock_rag = MockRag.return_value
        mock_rag.ask_document.return_value = (
            "This is a mocked answer.",
            0.95,
            [{"chunk_id": 1, "score": 0.95, "document_id": doc_id}]
        )
        
        response = client.post(
            f"/api/v1/documents/{doc_id}/ask",
            json={"question": "What is the answer?"}
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["answer"] == "This is a mocked answer."
        assert response.json()["data"]["confidence"] == 0.95

def test_ask_global_api_success():
    with patch('app.api.v1.rag.RagService') as MockRag:
        mock_rag = MockRag.return_value
        mock_rag.ask_global.return_value = (
            "Global mocked answer.",
            0.88,
            [{"chunk_id": 2, "score": 0.88, "document_id": str(uuid4())}]
        )
        
        response = client.post(
            "/api/v1/chat/rag",
            json={"question": "Global question?"}
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["answer"] == "Global mocked answer."
        assert response.json()["data"]["confidence"] == 0.88

def test_search_document_api_success():
    doc_id = str(uuid4())
    
    with patch('app.api.v1.rag.RetrievalService') as MockRetrieval:
        mock_retrieval = MockRetrieval.return_value
        mock_retrieval.search_document.return_value = [
            {"chunk": "test chunk", "score": 0.9, "chunk_id": 0, "document_id": doc_id}
        ]
        
        response = client.get(
            f"/api/v1/documents/{doc_id}/search?query=test"
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert len(response.json()["data"]["matches"]) == 1
