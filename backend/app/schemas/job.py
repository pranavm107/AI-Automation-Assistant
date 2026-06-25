from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

# Requests
class JobMatchRequest(BaseModel):
    document_id: UUID
    job_description: str

class JobRecommendationRequest(BaseModel):
    document_id: UUID

class CareerRoadmapRequest(BaseModel):
    document_id: UUID
    target_role: str

class JobCompareRequest(BaseModel):
    document_id: UUID
    job_description: str

# Responses
class JobMatchData(BaseModel):
    match_score: int
    matching_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]

class JobMatchResponse(BaseModel):
    success: bool
    data: JobMatchData

class JobRecommendation(BaseModel):
    role: str
    match: int
    reason: str

class JobRecommendationResponse(BaseModel):
    success: bool
    data: List[JobRecommendation]

class Milestone(BaseModel):
    month: str
    focus: str
    topics: List[str]

class CareerRoadmapData(BaseModel):
    target_role: str
    recommended_skills: List[str]
    milestones: List[Milestone]

class CareerRoadmapResponse(BaseModel):
    success: bool
    data: CareerRoadmapData

class JobCompareData(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    improvement_areas: List[str]

class JobCompareResponse(BaseModel):
    success: bool
    data: JobCompareData
