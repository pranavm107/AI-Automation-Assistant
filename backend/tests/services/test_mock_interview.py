import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.mock_interview_service import MockInterviewService

def test_create_mock_interview():
    doc_id = uuid4()
    
    with patch('app.services.mock_interview_service.InterviewGeneratorService') as MockGenerator:
        with patch('app.services.mock_interview_service.ResumeParserService') as MockParser:
            with patch('app.services.mock_interview_service.GeminiService') as MockGemini:
                
                mock_generator = MockGenerator.return_value
                mock_generator.generate_interview_set.return_value = [
                    {"question": "Q1", "expected_answer": "A1", "evaluation_criteria": [], "difficulty": "Medium", "category": "Technical"}
                ]
                
                mock_parser = MockParser.return_value
                mock_parser.parse_resume.return_value = {"category": "Experienced"}
                mock_parser.extract_name.return_value = "Jane Doe"
                
                mock_gemini = MockGemini.return_value
                mock_gemini.generate_response.return_value = '{"introduction": "Welcome Jane.", "preparation_tips": ["Relax."]}'
                
                service = MockInterviewService()
                # Inject mocked dependencies
                service.generator_service = mock_generator
                service.parser_service = mock_parser
                service.gemini_service = mock_gemini
                
                mock_data = service.create_mock_interview(doc_id, "Developer")
                
                assert mock_data["introduction"] == "Welcome Jane."
                assert len(mock_data["questions"]) == 1
                assert mock_data["questions"][0]["question"] == "Q1"
                assert mock_data["preparation_tips"] == ["Relax."]

def test_create_mock_interview_gemini_fallback():
    doc_id = uuid4()
    
    with patch('app.services.mock_interview_service.InterviewGeneratorService') as MockGenerator:
        with patch('app.services.mock_interview_service.ResumeParserService') as MockParser:
            with patch('app.services.mock_interview_service.GeminiService') as MockGemini:
                
                mock_generator = MockGenerator.return_value
                mock_generator.generate_interview_set.return_value = []
                
                mock_parser = MockParser.return_value
                mock_parser.parse_resume.return_value = {}
                mock_parser.extract_name.return_value = "Jane Doe"
                
                mock_gemini = MockGemini.return_value
                mock_gemini.generate_response.return_value = 'Invalid JSON'
                
                service = MockInterviewService()
                service.generator_service = mock_generator
                service.parser_service = mock_parser
                service.gemini_service = mock_gemini
                
                mock_data = service.create_mock_interview(doc_id, "Developer")
                
                # Should fallback to default string
                assert "Jane Doe" in mock_data["introduction"]
                assert "Developer" in mock_data["introduction"]
