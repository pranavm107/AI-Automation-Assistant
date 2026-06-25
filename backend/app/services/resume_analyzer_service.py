import logging
import json
from uuid import UUID
from typing import Dict, Any, List, Tuple
from app.core.exceptions import AppError
from app.services.resume_parser_service import ResumeParserService
from app.services.ats_service import AtsService
from app.services.gemini_service import GeminiService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class ResumeAnalyzerService:
    def __init__(self, document_service: DocumentService = None):
        self.parser_service = ResumeParserService(document_service)
        self.ats_service = AtsService()
        self.gemini_service = GeminiService()

    def _clean_json_response(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def analyze_resume(self, document_id: UUID) -> Dict[str, Any]:
        """
        Analyzes a resume by parsing it, calculating ATS, and using Gemini for qualitative insights.
        Returns: Summary, Strengths, Weaknesses, Recommendations
        """
        logger.info(f"Analyzing resume {document_id}")
        
        # 1. Parse Resume
        parsed_data = self.parser_service.parse_resume(document_id)
        
        # 2. Get ATS Score internally to inform Gemini
        ats_score, breakdown, missing, improvements = self.ats_service.calculate_ats_score(parsed_data)
        
        # 3. Use Gemini for qualitative analysis
        prompt = f"""You are an expert tech recruiter and career coach.
Analyze the following parsed resume data and the calculated ATS metrics.
Output ONLY a valid JSON object matching the exact schema below. Do not use markdown backticks.

Schema:
{{
    "summary": "str (A 2-3 sentence professional summary of the candidate)",
    "strengths": ["str"],
    "weaknesses": ["str"],
    "recommendations": ["str (Actionable career or resume advice)"]
}}

Parsed Resume:
{json.dumps(parsed_data, indent=2)}

ATS Score: {ats_score}/100
ATS Improvements: {improvements}
"""
        logger.info("Sending resume analysis prompt to Gemini.")
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            analysis_data = json.loads(clean_json)
            return analysis_data
        except Exception as e:
            logger.error(f"Analysis Generation Failure: {e}", exc_info=True)
            raise AppError("Failed to generate qualitative analysis.", status_code=500)

    def analyze_skill_gap(self, document_id: UUID, target_role: str) -> Dict[str, Any]:
        """
        Compares extracted resume skills against a target role.
        """
        logger.info(f"Analyzing skill gap for {document_id} targeting {target_role}")
        
        # 1. Parse Resume
        parsed_data = self.parser_service.parse_resume(document_id)
        existing_skills = self.parser_service.extract_skills(parsed_data)
        
        if not existing_skills:
            # Try to handle gracefully
            existing_skills = ["No technical skills explicitly listed."]
            
        # 2. Use Gemini for Gap Analysis
        prompt = f"""You are a technical hiring manager evaluating a candidate for the role of: "{target_role}".
Below is the list of skills extracted from the candidate's resume.
Compare their skills to the industry standard requirements for a {target_role}.
Output ONLY a valid JSON object matching the exact schema below. Do not use markdown backticks.

Schema:
{{
    "existing_skills": ["str (Skills they have that are relevant)"],
    "missing_skills": ["str (Critical skills they lack for this role)"],
    "recommended_skills": ["str (Skills they should learn next to become highly competitive)"]
}}

Candidate's Current Skills:
{existing_skills}
"""
        logger.info("Sending skill gap prompt to Gemini.")
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            gap_data = json.loads(clean_json)
            
            # Fallback to existing skills if Gemini hallucinated empty
            if not gap_data.get("existing_skills"):
                gap_data["existing_skills"] = existing_skills
                
            return gap_data
        except Exception as e:
            logger.error(f"Skill Gap Generation Failure: {e}", exc_info=True)
            raise AppError("Failed to generate skill gap analysis.", status_code=500)

    def get_ats_score(self, document_id: UUID) -> Dict[str, Any]:
        """
        Public orchestrator for the ATS endpoint.
        """
        parsed_data = self.parser_service.parse_resume(document_id)
        score, breakdown, missing, improvements = self.ats_service.calculate_ats_score(parsed_data)
        
        return {
            "ats_score": score,
            "score_breakdown": breakdown,
            "missing_sections": missing,
            "improvements": improvements
        }
