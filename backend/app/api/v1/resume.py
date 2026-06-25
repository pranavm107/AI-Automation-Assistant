from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.session import get_db
from app.services.resume_analyzer_service import ResumeAnalyzerService
from app.services.document_service import DocumentService
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.resume import (
    ResumeRequest,
    SkillGapRequest,
    ResumeAnalysisResponse,
    ATSScoreResponse,
    SkillGapResponse
)

router = APIRouter(tags=["resume"])

@router.get("/health", description="Health check for Resume Analyzer")
def health_check():
    return {"status": "ok", "service": "Resume Analyzer"}

@router.post("/analyze", response_model=ResumeAnalysisResponse, description="Perform comprehensive qualitative analysis on a resume.")
def analyze_resume(request: ResumeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    analyzer_service = ResumeAnalyzerService(document_service)
    
    analysis_data = analyzer_service.analyze_resume(request.document_id)
    
    return ResumeAnalysisResponse(
        success=True,
        data=analysis_data
    )

@router.post("/ats-score", response_model=ATSScoreResponse, description="Calculate objective ATS metrics for a resume.")
def ats_score(request: ResumeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    analyzer_service = ResumeAnalyzerService(document_service)
    
    ats_data = analyzer_service.get_ats_score(request.document_id)
    
    return ATSScoreResponse(
        success=True,
        data=ats_data
    )

@router.post("/skill-gap", response_model=SkillGapResponse, description="Compare a resume against a target role for skill gaps.")
def skill_gap(request: SkillGapRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    analyzer_service = ResumeAnalyzerService(document_service)
    
    gap_data = analyzer_service.analyze_skill_gap(request.document_id, request.target_role)
    
    return SkillGapResponse(
        success=True,
        data=gap_data
    )
