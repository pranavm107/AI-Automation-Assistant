from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from app.core.exceptions import AppError

client = TestClient(app)

def test_valid_chat_request():
    with patch('app.services.gemini_service.GeminiService.generate_response') as mock_generate:
        mock_generate.return_value = "This is a mock response from Gemini."
        
        response = client.post("/api/v1/chat", json={"message": "Hello AI"})
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["answer"] == "This is a mock response from Gemini."

def test_empty_message():
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422 # FastAPI validation error

def test_invalid_payload():
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422 # FastAPI validation error

def test_gemini_failure():
    with patch('app.services.gemini_service.GeminiService.generate_response') as mock_generate:
        mock_generate.side_effect = AppError("Failed to generate response from AI.", status_code=500)
        
        response = client.post("/api/v1/chat", json={"message": "Fail me"})
        
        assert response.status_code == 500
        assert response.json()["success"] is False
        assert response.json()["message"] == "Failed to generate response from AI."
