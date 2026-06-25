from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/interview/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Interview Generator"}

def test_generate_questions_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.interview.InterviewGeneratorService') as MockService:
        mock_service = MockService.return_value
        mock_service.generate_interview_set.return_value = [
            {"question": "Q1", "expected_answer": "A1", "evaluation_criteria": ["C1"], "difficulty": "Medium", "category": "Technical"}
        ]
        
        response = client.post("/api/v1/interview/generate", json={
            "document_id": doc_id,
            "role": "Developer",
            "difficulty": "Medium",
            "question_count": 5
        })
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert len(response.json()["data"]["questions"]) == 1
        assert response.json()["data"]["questions"][0]["question"] == "Q1"

def test_mock_interview_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.interview.MockInterviewService') as MockService:
        mock_service = MockService.return_value
        mock_service.create_mock_interview.return_value = {
            "introduction": "Welcome.",
            "questions": [],
            "preparation_tips": ["Tip 1"]
        }
        
        response = client.post("/api/v1/interview/mock", json={
            "document_id": doc_id,
            "role": "Developer"
        })
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["introduction"] == "Welcome."
        assert response.json()["data"]["preparation_tips"] == ["Tip 1"]
