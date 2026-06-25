import logging
import json
from uuid import UUID
from typing import Dict, Any, List
from app.core.exceptions import AppError
from app.services.gemini_service import GeminiService
from app.services.resume_parser_service import ResumeParserService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

SUPPORTED_ROLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Python Developer",
    "Backend Developer",
    "Full Stack Developer",
    "AI Intern",
    "ML Intern",
    "Software Engineer",
    "Data Analyst"
]

class JobRecommendationService:
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

    def recommend_jobs(self, document_id: UUID) -> List[Dict[str, Any]]:
        """
        Recommends suitable roles from the SUPPORTED_ROLES list based on the candidate's resume.
        """
        logger.info(f"Generating job recommendations for {document_id}")
        
        parsed_resume = self.parser_service.parse_resume(document_id)
        
        prompt = f"""You are an expert Career Counselor.
Review the following candidate's resume data.
Evaluate their fit against the following specific list of supported roles:
{SUPPORTED_ROLES}

Select the Top 3 best matching roles for this candidate.
Output ONLY a valid JSON array of objects.

Schema for each object:
{{
  "role": "str (MUST be from the supported roles list)",
  "match": "int (0-100 estimated match percentage based on their skills)",
  "reason": "str (1-2 sentences explaining why this role is a good fit)"
}}

Candidate Resume Data:
{json.dumps(parsed_resume)}
"""
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            recommendations = json.loads(clean_json)
            
            if not isinstance(recommendations, list):
                raise ValueError("Expected JSON array")
                
            # Filter out hallucinations
            valid_recs = []
            for rec in recommendations:
                if rec.get("role") in SUPPORTED_ROLES:
                    valid_recs.append(rec)
                    
            # Sort by match descending
            valid_recs.sort(key=lambda x: x.get("match", 0), reverse=True)
            return valid_recs
            
        except Exception as e:
            logger.error(f"Failed to generate job recommendations: {e}")
            raise AppError("Failed to generate job recommendations.", status_code=500)
