import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.interview_generator_service import InterviewGeneratorService

def test_clean_json_response():
    service = InterviewGeneratorService()
    raw = "```json\n[{\"q\": \"1\"}]\n```"
    clean = service._clean_json_response(raw)
    assert clean == "[{\"q\": \"1\"}]"

def test_generate_technical_questions():
    doc_id = uuid4()
    
    with patch('app.services.interview_generator_service.ResumeParserService') as MockParser:
        with patch('app.services.interview_generator_service.GeminiService') as MockGemini:
            mock_parser = MockParser.return_value
            mock_parser.parse_resume.return_value = {}
            mock_parser.extract_skills.return_value = ["Python", "FastAPI"]
            
            mock_gemini = MockGemini.return_value
            # We mock the Gemini raw response to return a JSON array
            mock_gemini.generate_response.return_value = '''[
                {
                    "question": "What is FastAPI?",
                    "expected_answer": "A modern web framework.",
                    "evaluation_criteria": ["Mentions speed", "Mentions async"],
                    "difficulty": "Easy",
                    "category": "Technical"
                }
            ]'''
            
            service = InterviewGeneratorService()
            # Inject mocked dependencies
            service.parser_service = mock_parser
            service.gemini_service = mock_gemini
            
            questions = service.generate_technical_questions(doc_id, "Python Developer", "Easy", 1)
            
            assert len(questions) == 1
            assert questions[0]["question"] == "What is FastAPI?"
            assert questions[0]["difficulty"] == "Easy"
            assert questions[0]["category"] == "Technical"

def test_generate_interview_set():
    doc_id = uuid4()
    
    with patch.object(InterviewGeneratorService, 'generate_technical_questions') as mock_tech:
        with patch.object(InterviewGeneratorService, 'generate_hr_questions') as mock_hr:
            with patch.object(InterviewGeneratorService, 'generate_project_questions') as mock_proj:
                with patch.object(InterviewGeneratorService, 'generate_role_questions') as mock_role:
                    
                    mock_tech.return_value = [{"category": "Technical"}]
                    mock_hr.return_value = [{"category": "HR"}]
                    mock_proj.return_value = [{"category": "Project"}]
                    mock_role.return_value = [{"category": "Role"}]
                    
                    service = InterviewGeneratorService()
                    # Generate a set of 4 questions total
                    questions = service.generate_interview_set(doc_id, "Role", "Medium", 4)
                    
                    assert len(questions) == 4
                    categories = [q["category"] for q in questions]
                    assert "Technical" in categories
                    assert "HR" in categories
                    assert "Project" in categories
                    assert "Role" in categories
