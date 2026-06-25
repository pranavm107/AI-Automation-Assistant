import logging
import json
from typing import Dict, Any, List
from uuid import UUID
from app.core.exceptions import AppError
from app.services.gemini_service import GeminiService
from app.services.resume_parser_service import ResumeParserService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class InterviewGeneratorService:
    def __init__(self, document_service: DocumentService = None):
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

    def _generate_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Core method to generate questions using Gemini and enforce strict JSON array output."""
        full_prompt = f"""{prompt}
        
Output ONLY a valid JSON array of objects. Do not include markdown formatting or backticks.
Schema for each object in the array:
{{
    "question": "str (The interview question)",
    "expected_answer": "str (A comprehensive model answer)",
    "evaluation_criteria": ["str (Points the interviewer should look for)"],
    "difficulty": "str (Easy, Medium, or Hard)",
    "category": "str (Technical, HR, Project, or Role)"
}}
"""
        logger.info("Sending interview generation prompt to Gemini.")
        try:
            response_text = self.gemini_service.generate_response(full_prompt)
            clean_json = self._clean_json_response(response_text)
            questions = json.loads(clean_json)
            if not isinstance(questions, list):
                raise ValueError("Expected a JSON array of questions.")
            return questions
        except Exception as e:
            logger.error(f"Failed to generate questions: {e}", exc_info=True)
            raise AppError("Question Generation Failure.", status_code=500)

    def generate_technical_questions(self, document_id: UUID, role: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        logger.info(f"Generating {count} {difficulty} technical questions for {role}")
        parsed_data = self.parser_service.parse_resume(document_id)
        skills = self.parser_service.extract_skills(parsed_data)
        
        prompt = f"""You are an expert technical interviewer hiring a {role}.
The candidate claims the following technical skills: {skills}.
Generate {count} Technical interview questions tailored to these specific skills at a {difficulty} difficulty level.
The category must be "Technical".
"""
        return self._generate_questions(prompt)

    def generate_hr_questions(self, document_id: UUID, difficulty: str, count: int) -> List[Dict[str, Any]]:
        logger.info(f"Generating {count} {difficulty} HR questions")
        parsed_data = self.parser_service.parse_resume(document_id)
        category = parsed_data.get("category", "Experienced")
        
        prompt = f"""You are an expert HR recruiter.
The candidate is classified as: {category}.
Generate {count} behavioral/HR interview questions at a {difficulty} difficulty level suitable for this experience level.
Include common themes like teamwork, conflict resolution, or leadership.
The category must be "HR".
"""
        return self._generate_questions(prompt)

    def generate_project_questions(self, document_id: UUID, difficulty: str, count: int) -> List[Dict[str, Any]]:
        logger.info(f"Generating {count} {difficulty} project questions")
        parsed_data = self.parser_service.parse_resume(document_id)
        projects = self.parser_service.extract_projects(parsed_data)
        
        if not projects:
            # Fallback if no projects exist
            return self.generate_technical_questions(document_id, "Software Engineer", difficulty, count)
            
        prompt = f"""You are a technical hiring manager.
The candidate listed the following projects on their resume:
{json.dumps(projects, indent=2)}

Generate {count} specific questions interrogating these exact projects (e.g., asking about architecture, challenges, or specific technical decisions made) at a {difficulty} difficulty level.
The category must be "Project".
"""
        return self._generate_questions(prompt)

    def generate_role_questions(self, role: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        logger.info(f"Generating {count} {difficulty} role questions for {role}")
        
        prompt = f"""You are an industry expert in the {role} field.
Generate {count} industry-standard interview questions specifically targeting core competencies for a {role} at a {difficulty} difficulty level.
Do not make them general programming questions; make them highly specific to the domain of a {role}.
The category must be "Role".
"""
        return self._generate_questions(prompt)

    def generate_interview_set(self, document_id: UUID, role: str, difficulty: str, question_count: int) -> List[Dict[str, Any]]:
        """Generates a dynamic mix of questions for a generalized interview prep set."""
        # Distribute the count roughly: 40% Tech, 20% HR, 20% Project, 20% Role
        tech_count = max(1, int(question_count * 0.4))
        hr_count = max(1, int(question_count * 0.2))
        proj_count = max(1, int(question_count * 0.2))
        role_count = question_count - (tech_count + hr_count + proj_count)
        if role_count < 0: role_count = 0
        
        questions = []
        if tech_count > 0: questions.extend(self.generate_technical_questions(document_id, role, difficulty, tech_count))
        if hr_count > 0: questions.extend(self.generate_hr_questions(document_id, difficulty, hr_count))
        if proj_count > 0: questions.extend(self.generate_project_questions(document_id, difficulty, proj_count))
        if role_count > 0: questions.extend(self.generate_role_questions(role, difficulty, role_count))
        
        return questions[:question_count]
