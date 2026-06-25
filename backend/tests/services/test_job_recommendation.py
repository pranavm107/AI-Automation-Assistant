import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from app.services.job_recommendation_service import JobRecommendationService

def test_recommend_jobs():
    doc_id = uuid4()
    
    with patch('app.services.job_recommendation_service.ResumeParserService') as MockParser:
        with patch('app.services.job_recommendation_service.GeminiService') as MockGemini:
            mock_parser = MockParser.return_value
            mock_parser.parse_resume.return_value = {"skills": ["Python"]}
            
            mock_gemini = MockGemini.return_value
            mock_gemini.generate_response.return_value = '''[
                {"role": "Python Developer", "match": 95, "reason": "Good"},
                {"role": "Backend Developer", "match": 80, "reason": "Okay"},
                {"role": "Invalid Role Name", "match": 100, "reason": "Will be filtered"}
            ]'''
            
            service = JobRecommendationService()
            service.parser_service = mock_parser
            service.gemini_service = mock_gemini
            
            recs = service.recommend_jobs(doc_id)
            
            # The invalid role should be filtered out
            assert len(recs) == 2
            assert recs[0]["role"] == "Python Developer"
            assert recs[0]["match"] == 95
