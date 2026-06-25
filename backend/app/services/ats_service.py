import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class AtsService:
    def calculate_ats_score(self, parsed_data: Dict[str, Any]) -> Tuple[int, Dict[str, int], List[str], List[str]]:
        """
        Calculates deterministic ATS readiness score based on the extracted JSON fields.
        Returns: Total Score (0-100), Breakdown Dictionary, Missing Sections, Improvement Suggestions.
        """
        logger.info("Calculating ATS Score")
        
        score = 0
        breakdown = {}
        missing_sections = []
        improvements = []

        # 1. Contact Info (max 10)
        contact = parsed_data.get("contact", {})
        contact_score = 0
        if contact.get("name"): contact_score += 4
        if contact.get("email"): contact_score += 3
        else: improvements.append("Add a professional email address.")
        if contact.get("phone"): contact_score += 3
        else: improvements.append("Include a contact phone number.")
        
        breakdown["Contact Info"] = contact_score
        score += contact_score
        if contact_score == 0: missing_sections.append("Contact Information")

        # 2. Skills Section (max 20)
        skills = parsed_data.get("skills", [])
        skills_score = min(20, len(skills) * 2) # 2 points per skill, up to 20
        breakdown["Skills"] = skills_score
        score += skills_score
        if not skills:
            missing_sections.append("Skills")
            improvements.append("Add a dedicated skills section outlining your technical and soft skills.")
        elif len(skills) < 5:
            improvements.append("Expand your skills section. List at least 5-10 core competencies.")

        # 3. Projects (max 20)
        projects = parsed_data.get("projects", [])
        projects_score = min(20, len(projects) * 10) # 10 points per project, up to 20
        breakdown["Projects"] = projects_score
        score += projects_score
        if not projects:
            missing_sections.append("Projects")
            improvements.append("Include 1-2 major projects showcasing practical experience.")

        # 4. Education (max 15)
        education = parsed_data.get("education", [])
        edu_score = 15 if education else 0
        breakdown["Education"] = edu_score
        score += edu_score
        if not education:
            missing_sections.append("Education")
            improvements.append("Add your education history, even if currently ongoing.")

        # 5. Certifications (max 10)
        certs = parsed_data.get("certifications", [])
        cert_score = min(10, len(certs) * 5)
        breakdown["Certifications"] = cert_score
        score += cert_score
        if not certs:
            improvements.append("Consider adding relevant certifications to boost ATS visibility.")

        # 6. Keywords/Density (max 15)
        # We simulate keyword density by checking total text volume across lists
        total_items = len(skills) + len(projects)*3 + len(parsed_data.get("experience", []))*3
        keyword_score = min(15, total_items)
        breakdown["Keywords"] = keyword_score
        score += keyword_score
        if keyword_score < 10:
            improvements.append("Increase keyword density by detailing your project bullet points and experience descriptions.")

        # 7. Formatting & Completeness (max 10)
        # Check if we have the critical trifecta: Contact, Skills, and (Projects OR Experience)
        experience = parsed_data.get("experience", [])
        format_score = 10 if (contact_score >= 7 and skills and (projects or experience)) else 5
        breakdown["Formatting & Completeness"] = format_score
        score += format_score
        
        if format_score < 10:
            improvements.append("Ensure your resume has standard, parsable headers for Contact, Skills, and Experience.")

        logger.info(f"Final ATS Score: {score}/100")
        
        return score, breakdown, missing_sections, improvements
