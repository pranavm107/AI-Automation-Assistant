from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class GenerateRequest(BaseModel):
    document_id: UUID
    role: str
    difficulty: str = Field(default="Medium", pattern="^(Easy|Medium|Hard)$")
    question_count: int = Field(default=5, ge=1, le=20)

class MockRequest(BaseModel):
    document_id: UUID
    role: str

class InterviewQuestion(BaseModel):
    question: str
    expected_answer: str
    evaluation_criteria: List[str]
    difficulty: str
    category: str

class QuestionListResponseData(BaseModel):
    questions: List[InterviewQuestion]

class QuestionListResponse(BaseModel):
    success: bool
    data: QuestionListResponseData

class MockInterviewSession(BaseModel):
    introduction: str
    questions: List[InterviewQuestion]
    preparation_tips: List[str]

class MockInterviewResponse(BaseModel):
    success: bool
    data: MockInterviewSession
