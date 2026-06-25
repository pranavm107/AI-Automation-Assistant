import logging
import json
from uuid import UUID
from typing import Dict, Any, List
from app.core.exceptions import AppError
from app.services.gemini_service import GeminiService
from app.services.resume_parser_service import ResumeParserService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class CareerRoadmapService:
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

    def generate_roadmap(self, document_id: UUID, target_role: str) -> Dict[str, Any]:
        """
        Generates a structured learning roadmap to bridge the gap between current skills and a target role.
        """
        logger.info(f"Generating career roadmap for {document_id} targeting {target_role}")
        
        parsed_resume = self.parser_service.parse_resume(document_id)
        current_skills = self.parser_service.extract_skills(parsed_resume)
        
        prompt = f"""You are an expert Career Coach and Technical Mentor.
A candidate wants to become a "{target_role}".
Their current skills are: {current_skills}.

Generate a 6-month learning roadmap bridging the gap between their current skills and the target role.
Break the roadmap down month-by-month, specifying exact technologies, milestones, and recommended skills to acquire.

Output ONLY a valid JSON object. Do not include markdown backticks.

Schema:
{{
  "target_role": "{target_role}",
  "recommended_skills": ["str (Master list of skills to learn)"],
  "milestones": [
    {{
      "month": "str (e.g., 'Month 1')",
      "focus": "str (The overarching theme)",
      "topics": ["str (Specific topics or tools to learn)"]
    }}
  ]
}}
"""
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            roadmap = json.loads(clean_json)
            
            # Ensure target_role is explicitly set
            roadmap["target_role"] = target_role
            return roadmap
            
        except Exception as e:
            logger.error(f"Failed to generate roadmap: {e}")
            raise AppError("Failed to generate career roadmap.", status_code=500)
