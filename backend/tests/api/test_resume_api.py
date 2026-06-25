from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/resume/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Resume Analyzer"}

def test_analyze_resume_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.resume.ResumeAnalyzerService') as MockService:
        mock_service = MockService.return_value
        mock_service.analyze_resume.return_value = {
            "summary": "API Summary",
            "strengths": ["S1"],
            "weaknesses": ["W1"],
            "recommendations": ["R1"]
        }
        
        response = client.post("/api/v1/resume/analyze", json={"document_id": doc_id})
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["data"]["summary"] == "API Summary"

def test_ats_score_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.resume.ResumeAnalyzerService') as MockService:
        mock_service = MockService.return_value
        mock_service.get_ats_score.return_value = {
            "ats_score": 85,
            "score_breakdown": {"Skills": 20},
            "missing_sections": [],
            "improvements": []
        }
        
        response = client.post("/api/v1/resume/ats-score", json={"document_id": doc_id})
        
        assert response.status_code == 200
        assert response.json()["data"]["ats_score"] == 85

def test_skill_gap_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.resume.ResumeAnalyzerService') as MockService:
        mock_service = MockService.return_value
        mock_service.analyze_skill_gap.return_value = {
            "existing_skills": ["Python"],
            "missing_skills": ["C++"],
            "recommended_skills": ["C++"]
        }
        
        response = client.post("/api/v1/resume/skill-gap", json={
            "document_id": doc_id,
            "target_role": "Developer"
        })
        
        assert response.status_code == 200
        assert response.json()["data"]["missing_skills"] == ["C++"]
