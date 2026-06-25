import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.resume_parser_service import ResumeParserService
from app.core.exceptions import AppError

def test_clean_json_response():
    service = ResumeParserService()
    raw = "```json\n{\"name\": \"John\"}\n```"
    clean = service._clean_json_response(raw)
    assert clean == "{\"name\": \"John\"}"

def test_parse_resume_success():
    doc_id = uuid4()
    
    with patch('app.services.resume_parser_service.GeminiService') as MockGemini:
        with patch('app.services.resume_parser_service.DocumentService') as MockDoc:
            mock_doc_service = MockDoc.return_value
            mock_content = MagicMock()
            mock_content.data.chunks = ["John Doe", "Software Engineer"]
            mock_doc_service.get_document_content.return_value = mock_content
            
            mock_gemini_service = MockGemini.return_value
            mock_gemini_service.generate_response.return_value = '{"contact": {"name": "John Doe"}, "skills": ["Python"]}'
            
            service = ResumeParserService(document_service=mock_doc_service)
            parsed_data = service.parse_resume(doc_id)
            
            assert parsed_data["contact"]["name"] == "John Doe"
            assert parsed_data["skills"][0] == "Python"
            
            # Test Extractors
            assert service.extract_name(parsed_data) == "John Doe"
            assert service.extract_skills(parsed_data) == ["Python"]

def test_parse_resume_invalid_json():
    doc_id = uuid4()
    
    with patch('app.services.resume_parser_service.GeminiService') as MockGemini:
        with patch('app.services.resume_parser_service.DocumentService') as MockDoc:
            mock_doc_service = MockDoc.return_value
            mock_content = MagicMock()
            mock_content.data.chunks = ["John Doe", "Software Engineer"]
            mock_doc_service.get_document_content.return_value = mock_content
            
            mock_gemini_service = MockGemini.return_value
            mock_gemini_service.generate_response.return_value = 'Not JSON at all'
            
            service = ResumeParserService(document_service=mock_doc_service)
            with pytest.raises(AppError) as exc_info:
                service.parse_resume(doc_id)
            assert exc_info.value.status_code == 500
