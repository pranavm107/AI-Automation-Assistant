import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from app.services.resume_analyzer_service import ResumeAnalyzerService

def test_analyze_resume_success():
    doc_id = uuid4()
    
    with patch('app.services.resume_analyzer_service.ResumeParserService') as MockParser:
        with patch('app.services.resume_analyzer_service.AtsService') as MockAts:
            with patch('app.services.resume_analyzer_service.GeminiService') as MockGemini:
                mock_parser = MockParser.return_value
                mock_parser.parse_resume.return_value = {"contact": {"name": "Test"}}
                
                mock_ats = MockAts.return_value
                mock_ats.calculate_ats_score.return_value = (80, {}, [], [])
                
                mock_gemini = MockGemini.return_value
                mock_gemini.generate_response.return_value = '{"summary": "A good resume", "strengths": ["S1"], "weaknesses": ["W1"], "recommendations": ["R1"]}'
                
                service = ResumeAnalyzerService()
                # Inject mocked dependencies
                service.parser_service = mock_parser
                service.ats_service = mock_ats
                service.gemini_service = mock_gemini
                
                analysis = service.analyze_resume(doc_id)
                
                assert analysis["summary"] == "A good resume"
                assert analysis["strengths"] == ["S1"]

def test_analyze_skill_gap_success():
    doc_id = uuid4()
    
    with patch('app.services.resume_analyzer_service.ResumeParserService') as MockParser:
        with patch('app.services.resume_analyzer_service.GeminiService') as MockGemini:
            mock_parser = MockParser.return_value
            mock_parser.parse_resume.return_value = {}
            mock_parser.extract_skills.return_value = ["Python"]
            
            mock_gemini = MockGemini.return_value
            mock_gemini.generate_response.return_value = '{"existing_skills": ["Python"], "missing_skills": ["Java"], "recommended_skills": ["Java"]}'
            
            service = ResumeAnalyzerService()
            service.parser_service = mock_parser
            service.gemini_service = mock_gemini
            
            gap = service.analyze_skill_gap(doc_id, "Java Developer")
            
            assert gap["existing_skills"] == ["Python"]
            assert gap["missing_skills"] == ["Java"]
