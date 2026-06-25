import pytest
from unittest.mock import patch
from uuid import uuid4
from app.services.career_roadmap_service import CareerRoadmapService

def test_generate_roadmap():
    doc_id = uuid4()
    
    with patch('app.services.career_roadmap_service.ResumeParserService') as MockParser:
        with patch('app.services.career_roadmap_service.GeminiService') as MockGemini:
            mock_parser = MockParser.return_value
            mock_parser.parse_resume.return_value = {}
            mock_parser.extract_skills.return_value = ["Python"]
            
            mock_gemini = MockGemini.return_value
            mock_gemini.generate_response.return_value = '''{
                "target_role": "AI Engineer",
                "recommended_skills": ["TensorFlow"],
                "milestones": [{"month": "Month 1", "focus": "Basics", "topics": ["Linear Algebra"]}]
            }'''
            
            service = CareerRoadmapService()
            service.parser_service = mock_parser
            service.gemini_service = mock_gemini
            
            roadmap = service.generate_roadmap(doc_id, "AI Engineer")
            
            assert roadmap["target_role"] == "AI Engineer"
            assert "TensorFlow" in roadmap["recommended_skills"]
            assert len(roadmap["milestones"]) == 1
