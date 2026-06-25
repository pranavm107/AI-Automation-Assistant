from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.services.rag_service import RagService
from app.services.retrieval_service import RetrievalService
from app.repositories.document_repository import DocumentRepository
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.rag import (
    RAGQuestionRequest,
    RAGAnswerResponse,
    RAGAnswerData,
    SearchResponse,
    SearchData,
    RetrievalMatch,
    SourceReference
)

router = APIRouter(tags=["rag"])

@router.post("/documents/{document_id}/ask", response_model=RAGAnswerResponse, description="Ask a question against a single document using RAG.")
def ask_document(document_id: UUID, request: RAGQuestionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rag_service = RagService(document_repository=DocumentRepository(db, current_user.id))
    
    answer, confidence, sources = rag_service.ask_document(str(document_id), request.question)
    
    source_references = [SourceReference(**source) for source in sources]
    
    return RAGAnswerResponse(
        success=True,
        data=RAGAnswerData(
            answer=answer,
            confidence=confidence,
            sources=source_references
        )
    )

@router.post("/chat/rag", response_model=RAGAnswerResponse, description="Ask a question globally across all indexed documents.")
def ask_global(request: RAGQuestionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rag_service = RagService(document_repository=DocumentRepository(db, current_user.id))
    
    answer, confidence, sources = rag_service.ask_global(request.question)
    
    source_references = [SourceReference(**source) for source in sources]
    
    return RAGAnswerResponse(
        success=True,
        data=RAGAnswerData(
            answer=answer,
            confidence=confidence,
            sources=source_references
        )
    )

@router.get("/documents/{document_id}/search", response_model=SearchResponse, description="Raw FAISS similarity search for debugging retrieval.")
def search_document(document_id: UUID, query: str, db: Session = Depends(get_db)):
    retrieval_service = RetrievalService()
    
    matches = retrieval_service.search_document(str(document_id), query, top_k=5)
    
    retrieval_matches = [RetrievalMatch(**match) for match in matches]
    
    return SearchResponse(
        success=True,
        data=SearchData(matches=retrieval_matches)
    )
