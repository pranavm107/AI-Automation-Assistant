import logging
import json
import re
from typing import Dict, Any, List
from app.core.exceptions import AppError
from app.services.gemini_service import GeminiService
from app.services.document_service import DocumentService
from uuid import UUID

logger = logging.getLogger(__name__)

class ResumeParserService:
    def __init__(self, document_service: DocumentService = None):
        self.gemini_service = GeminiService()
        self.document_service = document_service

    def _clean_json_response(self, text: str) -> str:
        """Removes markdown code block syntax if Gemini returns it."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def parse_resume(self, document_id: UUID) -> Dict[str, Any]:
        """
        Fetches the document text and uses Gemini to extract structured JSON data.
        """
        logger.info(f"Parsing resume for document {document_id}")
        
        if not self.document_service:
            raise AppError("DocumentService not provided to ResumeParserService", status_code=500)
            
        content_res = self.document_service.get_document_content(document_id)
        if not content_res.data.chunks:
            raise AppError("Document has no text chunks to parse.", status_code=400)
            
        full_text = "\n".join(content_res.data.chunks)
        
        prompt = f"""You are an expert ATS (Applicant Tracking System) parser.
Extract the following information from the resume text provided below.
You MUST output ONLY a valid, raw JSON object (no markdown, no backticks, no conversational text) matching the exact schema below.

Schema:
{{
  "contact": {{
    "name": "str",
    "email": "str",
    "phone": "str"
  }},
  "skills": ["str"],
  "education": [
    {{
      "institution": "str",
      "degree": "str",
      "graduation_year": "str"
    }}
  ],
  "projects": [
    {{
      "name": "str",
      "description": "str"
    }}
  ],
  "certifications": ["str"],
  "experience": [
    {{
      "company": "str",
      "title": "str",
      "duration": "str",
      "description": "str"
    }}
  ],
  "category": "str (must be one of: Student, Fresher, Intern, Experienced)"
}}

Resume Text:
{full_text}"""

        logger.info("Sending resume extraction prompt to Gemini.")
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            parsed_data = json.loads(clean_json)
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode Gemini JSON response: {e}\nResponse: {response_text}")
            raise AppError("Failed to parse resume into structured data. Invalid JSON returned by AI.", status_code=500)
        except Exception as e:
            logger.error(f"Resume parsing failed: {e}", exc_info=True)
            raise AppError("Resume Parsing Failure", status_code=500)

    # Individual Extractor Methods
    def extract_name(self, parsed_data: Dict[str, Any]) -> str:
        return parsed_data.get("contact", {}).get("name", "")

    def extract_email(self, parsed_data: Dict[str, Any]) -> str:
        return parsed_data.get("contact", {}).get("email", "")

    def extract_phone(self, parsed_data: Dict[str, Any]) -> str:
        return parsed_data.get("contact", {}).get("phone", "")

    def extract_skills(self, parsed_data: Dict[str, Any]) -> List[str]:
        return parsed_data.get("skills", [])

    def extract_education(self, parsed_data: Dict[str, Any]) -> List[Dict[str, str]]:
        return parsed_data.get("education", [])

    def extract_projects(self, parsed_data: Dict[str, Any]) -> List[Dict[str, str]]:
        return parsed_data.get("projects", [])

    def extract_certifications(self, parsed_data: Dict[str, Any]) -> List[str]:
        return parsed_data.get("certifications", [])
        
    def extract_experience(self, parsed_data: Dict[str, Any]) -> List[Dict[str, str]]:
        return parsed_data.get("experience", [])
