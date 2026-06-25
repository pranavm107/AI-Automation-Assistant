from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.job_matching_service import JobMatchingService
from app.services.job_recommendation_service import JobRecommendationService
from app.services.career_roadmap_service import CareerRoadmapService
from app.services.document_service import DocumentService
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.job import (
    JobMatchRequest,
    JobMatchResponse,
    JobRecommendationRequest,
    JobRecommendationResponse,
    CareerRoadmapRequest,
    CareerRoadmapResponse,
    JobCompareRequest,
    JobCompareResponse
)

router = APIRouter(tags=["job"])

@router.get("/health", description="Health check for Job Intelligence")
def health_check():
    return {"status": "ok", "service": "Job Intelligence Engine"}

@router.post("/match", response_model=JobMatchResponse, description="Match a resume against a specific job description.")
def match_job(request: JobMatchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    matching_service = JobMatchingService(document_service)
    
    match_data = matching_service.match_resume_to_job(
        document_id=request.document_id,
        job_description=request.job_description
    )
    
    return JobMatchResponse(success=True, data=match_data)

@router.post("/recommend", response_model=JobRecommendationResponse, description="Recommend jobs based on a resume.")
def recommend_jobs(request: JobRecommendationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    rec_service = JobRecommendationService(document_service)
    
    recs = rec_service.recommend_jobs(document_id=request.document_id)
    
    return JobRecommendationResponse(success=True, data=recs)

@router.post("/roadmap", response_model=CareerRoadmapResponse, description="Generate a learning roadmap for a target role.")
def generate_roadmap(request: CareerRoadmapRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    roadmap_service = CareerRoadmapService(document_service)
    
    roadmap_data = roadmap_service.generate_roadmap(
        document_id=request.document_id,
        target_role=request.target_role
    )
    
    return CareerRoadmapResponse(success=True, data=roadmap_data)

@router.post("/compare", response_model=JobCompareResponse, description="Side-by-side qualitative comparison of resume vs JD.")
def compare_job(request: JobCompareRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    matching_service = JobMatchingService(document_service)
    
    compare_data = matching_service.compare_resume_and_job(
        document_id=request.document_id,
        job_description=request.job_description
    )
    
    return JobCompareResponse(success=True, data=compare_data)
