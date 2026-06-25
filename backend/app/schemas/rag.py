from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RAGQuestionRequest(BaseModel):
    question: str

class SourceReference(BaseModel):
    chunk_id: int
    score: float
    document_id: Optional[UUID] = None

class RAGAnswerData(BaseModel):
    answer: str
    confidence: float
    sources: List[SourceReference]

class RAGAnswerResponse(BaseModel):
    success: bool
    data: RAGAnswerData

class RetrievalMatch(BaseModel):
    chunk: str
    score: float
    chunk_id: int
    document_id: Optional[UUID] = None

class SearchData(BaseModel):
    matches: List[RetrievalMatch]

class SearchResponse(BaseModel):
    success: bool
    data: SearchData
