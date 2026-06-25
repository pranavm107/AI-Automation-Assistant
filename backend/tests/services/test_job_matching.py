import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.job_matching_service import JobMatchingService

def test_calculate_match_score():
    service = JobMatchingService()
    
    parsed_resume = {
        "skills": ["Python", "Docker", "SQL", "AWS"],
        "projects": [{"name": "P1"}, {"name": "P2"}],
        "education": [{"degree": "BSc"}],
        "certifications": [{"name": "AWS Certified"}],
        "experience": [{"company": "Tech Corp"}]
    }
    
    parsed_jd = {
        "required_skills": ["Python", "AWS", "Kubernetes"],
        "preferred_skills": ["Docker"],
        "education": ["BSc"],
        "certifications": [],
        "experience": "2+ years"
    }
    
    # JD Requires 3 skills. Resume has 2 matching (Python, AWS).
    # Skill Ratio = 2/3. Skill Score = (2/3) * 40 = 26.
    # Projects: 2 * 10 = 20.
    # Edu = 10.
    # Cert = 10.
    # Exp = 10.
    # Keyword: Preferred skill Docker is present. +2 points.
    # Total expected: 26 + 20 + 10 + 10 + 10 + 2 = 78
    
    score, matching, missing = service.calculate_match_score(parsed_resume, parsed_jd)
    
    assert score == 78
    assert "python" in matching
    assert "aws" in matching
    assert "kubernetes" in missing

def test_extract_job_requirements():
    with patch('app.services.job_matching_service.GeminiService') as MockGemini:
        mock_gemini = MockGemini.return_value
        mock_gemini.generate_response.return_value = '{"role": "Dev", "required_skills": ["Java"]}'
        
        service = JobMatchingService()
        service.gemini_service = mock_gemini
        
        reqs = service.extract_job_requirements("Looking for Java Dev")
        assert reqs["role"] == "Dev"
        assert reqs["required_skills"] == ["Java"]
