import logging
import json
from uuid import UUID
from typing import Dict, Any, List, Tuple
from app.core.exceptions import AppError
from app.services.gemini_service import GeminiService
from app.services.resume_parser_service import ResumeParserService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class JobMatchingService:
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

    def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Parses raw JD text into structured JSON."""
        logger.info("Extracting requirements from Job Description.")
        prompt = f"""You are an expert technical recruiter parsing a Job Description.
Extract the requirements into a strictly formatted JSON object.
Output ONLY valid JSON.

Schema:
{{
  "role": "str",
  "required_skills": ["str"],
  "preferred_skills": ["str"],
  "education": ["str"],
  "certifications": ["str"],
  "experience": "str (e.g., '3+ years')"
}}

Job Description:
{job_description}
"""
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Failed to parse JD: {e}")
            raise AppError("Failed to parse Job Description.", status_code=500)

    def calculate_match_score(self, parsed_resume: Dict[str, Any], parsed_jd: Dict[str, Any]) -> Tuple[int, List[str], List[str]]:
        """
        Calculates a deterministic 100-point match score.
        Skill (40), Project (20), Edu (10), Cert (10), Exp (10), Keyword (10).
        """
        score = 0
        
        # 1. Skill Match (max 40)
        resume_skills = [s.lower() for s in parsed_resume.get("skills", [])]
        jd_skills = [s.lower() for s in parsed_jd.get("required_skills", [])]
        
        matching_skills = []
        missing_skills = []
        
        for skill in jd_skills:
            # Simple substring match for robustness (e.g. "python 3" matches "python")
            if any(skill in rs or rs in skill for rs in resume_skills):
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)
                
        skill_score = 0
        if jd_skills:
            skill_match_ratio = len(matching_skills) / len(jd_skills)
            skill_score = int(skill_match_ratio * 40)
        score += skill_score
        
        # 2. Project Relevance (max 20)
        # We give partial credit based on how many projects they have
        projects = parsed_resume.get("projects", [])
        project_score = min(20, len(projects) * 10)
        score += project_score
        
        # 3. Education Match (max 10)
        # If JD asks for education and they have any, grant points
        edu_score = 10 if parsed_resume.get("education") else 0
        score += edu_score
        
        # 4. Certifications (max 10)
        cert_score = 10 if parsed_resume.get("certifications") else 0
        score += cert_score
        
        # 5. Experience (max 10)
        exp_score = 10 if parsed_resume.get("experience") else 0
        score += exp_score
        
        # 6. Keyword Match (max 10)
        # Check JD preferred skills in resume
        pref_skills = [s.lower() for s in parsed_jd.get("preferred_skills", [])]
        keyword_score = 0
        for skill in pref_skills:
            if any(skill in rs or rs in skill for rs in resume_skills):
                keyword_score += 2
        score += min(10, keyword_score)
        
        return score, matching_skills, missing_skills

    def match_resume_to_job(self, document_id: UUID, job_description: str) -> Dict[str, Any]:
        logger.info(f"Matching resume {document_id} to provided JD.")
        
        parsed_resume = self.parser_service.parse_resume(document_id)
        parsed_jd = self.extract_job_requirements(job_description)
        
        score, matching, missing = self.calculate_match_score(parsed_resume, parsed_jd)
        
        # Generate dynamic recommendations based on score
        recs = []
        if score < 60:
            recs.append("This role is a stretch. Consider upskilling in the missing core requirements before applying.")
        elif score < 80:
            recs.append("Good match! Tailor your resume to specifically highlight the missing preferred skills if you have them.")
        else:
            recs.append("Excellent match! Ensure your projects heavily feature the required skills to guarantee an interview.")
            
        if missing:
            recs.append(f"Consider learning or emphasizing: {', '.join(missing[:3])}.")
            
        return {
            "match_score": score,
            "matching_skills": matching,
            "missing_skills": missing,
            "recommendations": recs
        }

    def compare_resume_and_job(self, document_id: UUID, job_description: str) -> Dict[str, Any]:
        """Qualitative side-by-side comparison using Gemini."""
        parsed_resume = self.parser_service.parse_resume(document_id)
        parsed_jd = self.extract_job_requirements(job_description)
        
        prompt = f"""You are an expert Career Coach.
Compare the following parsed Resume with the parsed Job Description.
Identify specifically what aligns well, what is missing, and areas for improvement.
Output ONLY a valid JSON object.

Schema:
{{
  "matched_skills": ["str"],
  "missing_skills": ["str"],
  "improvement_areas": ["str (Actionable advice to tailor the resume for this JD)"]
}}

Resume:
{json.dumps(parsed_resume)}

Job Description:
{json.dumps(parsed_jd)}
"""
        try:
            response_text = self.gemini_service.generate_response(prompt)
            clean_json = self._clean_json_response(response_text)
            return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Failed to generate qualitative comparison: {e}")
            raise AppError("Failed to generate JD comparison.", status_code=500)
