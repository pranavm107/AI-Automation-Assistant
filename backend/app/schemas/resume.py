from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import UUID

class ResumeRequest(BaseModel):
    document_id: UUID

class SkillGapRequest(BaseModel):
    document_id: UUID
    target_role: str

class AnalysisData(BaseModel):
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]

class ResumeAnalysisResponse(BaseModel):
    success: bool
    data: AnalysisData

class ATSData(BaseModel):
    ats_score: int
    score_breakdown: Dict[str, int]
    missing_sections: List[str]
    improvements: List[str]

class ATSScoreResponse(BaseModel):
    success: bool
    data: ATSData

class SkillGapData(BaseModel):
    existing_skills: List[str]
    missing_skills: List[str]
    recommended_skills: List[str]

class SkillGapResponse(BaseModel):
    success: bool
    data: SkillGapData
