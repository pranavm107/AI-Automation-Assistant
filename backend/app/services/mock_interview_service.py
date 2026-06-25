import logging
import json
from uuid import UUID
from typing import Dict, Any, List
from app.core.exceptions import AppError
from app.services.interview_generator_service import InterviewGeneratorService
from app.services.gemini_service import GeminiService
from app.services.resume_parser_service import ResumeParserService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class MockInterviewService:
    def __init__(self, document_service: DocumentService = None):
        self.generator_service = InterviewGeneratorService(document_service)
        self.gemini_service = GeminiService()
        self.parser_service = ResumeParserService(document_service)

    def _clean_json_response(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def create_mock_interview(self, document_id: UUID, role: str) -> Dict[str, Any]:
        """
        Orchestrates the creation of a complete mock interview session.
        """
        logger.info(f"Creating mock interview session for document {document_id} targeting {role}")
        
        # 1. Generate the questions (Standard 8-question set: 3 Tech, 2 HR, 2 Project, 1 Role)
        questions = self.generator_service.generate_interview_set(
            document_id=document_id,
            role=role,
            difficulty="Medium",
            question_count=8
        )
        
        # 2. Parse basic details for personalized intro
        parsed_data = self.parser_service.parse_resume(document_id)
        name = self.parser_service.extract_name(parsed_data) or "Candidate"
        
        # 3. Generate Introduction and Preparation Tips using Gemini
        prompt = f"""You are an expert Interview Coach.
You are preparing a mock interview session for a candidate named {name} for the role of {role}.
Based on their resume category ({parsed_data.get('category', 'Unknown')}), generate:
1. A welcoming introduction script that the "Interviewer" will say to start the session.
2. A list of 3-5 specific preparation tips tailored to someone aiming for a {role} position.

Output ONLY a valid JSON object matching this schema without markdown:
{{
    "introduction": "str",
    "preparation_tips": ["str"]
}}
"""
        logger.info("Generating mock interview wrapper.")
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            wrapper_data = json.loads(clean_json)
        except Exception as e:
            logger.error(f"Failed to generate mock wrapper: {e}")
            wrapper_data = {
                "introduction": f"Hello {name}, welcome to your mock interview for the {role} position. Let's begin.",
                "preparation_tips": ["Review your resume thoroughly.", "Practice coding aloud.", "Use the STAR method for behavioral questions."]
            }
            
        return {
            "introduction": wrapper_data["introduction"],
            "questions": questions,
            "preparation_tips": wrapper_data.get("preparation_tips", [])
        }
