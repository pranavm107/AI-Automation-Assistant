from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from uuid import uuid4

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/job/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Job Intelligence Engine"}

def test_match_job_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.job.JobMatchingService') as MockService:
        mock_service = MockService.return_value
        mock_service.match_resume_to_job.return_value = {
            "match_score": 90,
            "matching_skills": ["Python"],
            "missing_skills": [],
            "recommendations": []
        }
        
        response = client.post("/api/v1/job/match", json={
            "document_id": doc_id,
            "job_description": "We need Python."
        })
        
        assert response.status_code == 200
        assert response.json()["data"]["match_score"] == 90

def test_recommend_jobs_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.job.JobRecommendationService') as MockService:
        mock_service = MockService.return_value
        mock_service.recommend_jobs.return_value = [
            {"role": "Dev", "match": 80, "reason": "Good fit"}
        ]
        
        response = client.post("/api/v1/job/recommend", json={"document_id": doc_id})
        
        assert response.status_code == 200
        assert response.json()["data"][0]["role"] == "Dev"

def test_generate_roadmap_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.job.CareerRoadmapService') as MockService:
        mock_service = MockService.return_value
        mock_service.generate_roadmap.return_value = {
            "target_role": "Dev",
            "recommended_skills": [],
            "milestones": []
        }
        
        response = client.post("/api/v1/job/roadmap", json={
            "document_id": doc_id,
            "target_role": "Dev"
        })
        
        assert response.status_code == 200
        assert response.json()["data"]["target_role"] == "Dev"

def test_compare_job_api():
    doc_id = str(uuid4())
    with patch('app.api.v1.job.JobMatchingService') as MockService:
        mock_service = MockService.return_value
        mock_service.compare_resume_and_job.return_value = {
            "matched_skills": ["Python"],
            "missing_skills": ["C++"],
            "improvement_areas": []
        }
        
        response = client.post("/api/v1/job/compare", json={
            "document_id": doc_id,
            "job_description": "Python C++"
        })
        
        assert response.status_code == 200
        assert "C++" in response.json()["data"]["missing_skills"]
