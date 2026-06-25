from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.interview_generator_service import InterviewGeneratorService
from app.services.mock_interview_service import MockInterviewService
from app.services.document_service import DocumentService
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.interview import (
    GenerateRequest,
    MockRequest,
    QuestionListResponse,
    QuestionListResponseData,
    MockInterviewResponse
)

router = APIRouter(tags=["interview"])

@router.get("/health", description="Health check for Interview Generator")
def health_check():
    return {"status": "ok", "service": "Interview Generator"}

@router.post("/generate", response_model=QuestionListResponse, description="Generate a mix of customized interview questions.")
def generate_questions(request: GenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    generator_service = InterviewGeneratorService(document_service)
    
    questions = generator_service.generate_interview_set(
        document_id=request.document_id,
        role=request.role,
        difficulty=request.difficulty,
        question_count=request.question_count
    )
    
    return QuestionListResponse(
        success=True,
        data=QuestionListResponseData(questions=questions)
    )

@router.post("/project-based", response_model=QuestionListResponse, description="Generate project-specific interview questions.")
def generate_project_questions(request: GenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    generator_service = InterviewGeneratorService(document_service)
    
    questions = generator_service.generate_project_questions(
        document_id=request.document_id,
        difficulty=request.difficulty,
        count=request.question_count
    )
    
    return QuestionListResponse(
        success=True,
        data=QuestionListResponseData(questions=questions)
    )

@router.post("/hr", response_model=QuestionListResponse, description="Generate HR/Behavioral interview questions.")
def generate_hr_questions(request: GenerateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    generator_service = InterviewGeneratorService(document_service)
    
    questions = generator_service.generate_hr_questions(
        document_id=request.document_id,
        difficulty=request.difficulty,
        count=request.question_count
    )
    
    return QuestionListResponse(
        success=True,
        data=QuestionListResponseData(questions=questions)
    )

@router.post("/mock", response_model=MockInterviewResponse, description="Generate a complete mock interview session.")
def generate_mock_interview(request: MockRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    mock_service = MockInterviewService(document_service)
    
    mock_data = mock_service.create_mock_interview(
        document_id=request.document_id,
        role=request.role
    )
    
    return MockInterviewResponse(
        success=True,
        data=mock_data
    )
