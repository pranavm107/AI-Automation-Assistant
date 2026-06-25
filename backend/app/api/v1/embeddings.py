from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_validation_service import VectorValidationService
from app.schemas.embedding import (
    EmbeddingGenerationResponse, EmbeddingGenerationData,
    EmbeddingStatusResponse, EmbeddingStatusData
)

router = APIRouter(prefix="/documents/{document_id}/embeddings", tags=["embeddings"])

from app.core.permissions import get_current_user
from app.models.user import User

@router.post("", response_model=EmbeddingGenerationResponse, description="Generate embeddings for a processed document.")
def generate_embeddings(document_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    
    # Retrieves document content. If document is unprocessed, it will raise 400.
    content_response = document_service.get_document_content(document_id)
    chunks = content_response.data.chunks
    
    # Generate embeddings
    embedding_service = EmbeddingService()
    embeddings = embedding_service.generate_embeddings(chunks)
    
    # Validate embeddings
    expected_dim = embedding_service.get_embedding_dimension()
    VectorValidationService.validate_embeddings(embeddings, expected_dim)
    
    # Update DB with metadata (not storing vectors)
    model_name = embedding_service.get_model_name()
    document_service.repository.mark_embeddings_generated(document_id, model_name, expected_dim)
    
    return EmbeddingGenerationResponse(
        success=True,
        message="Embeddings generated successfully",
        data=EmbeddingGenerationData(
            document_id=document_id,
            embedding_model=model_name,
            embedding_dimension=expected_dim,
            chunk_count=len(chunks),
            vector_count=len(embeddings)
        )
    )

@router.get("/status", response_model=EmbeddingStatusResponse, description="Check embedding generation status.")
def get_embedding_status(document_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    doc = document_service.get_document_by_id(document_id) # Raises 404 if not found
    
    return EmbeddingStatusResponse(
        success=True,
        data=EmbeddingStatusData(
            embeddings_generated=doc.embeddings_generated,
            embedding_model=doc.embedding_model,
            embedding_dimension=doc.embedding_dimension,
            generated_at=doc.embeddings_generated_at
        )
    )
