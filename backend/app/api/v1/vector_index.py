from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.services.document_service import DocumentService
from app.services.vector_store_service import VectorStoreService
from app.repositories.document_repository import DocumentRepository
from app.core.permissions import get_current_user
from app.models.user import User
from app.schemas.vector_index import (
    VectorIndexResponse,
    VectorIndexStatusResponse,
    VectorIndexDeleteResponse
)

router = APIRouter(prefix="/documents/{document_id}/index", tags=["vector_index"])

@router.post("", response_model=VectorIndexResponse, description="Create FAISS index for document embeddings.")
def create_document_index(document_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_service = DocumentService(db, current_user.id)
    
    # Retrieves document content. If document is unprocessed, it will raise 400.
    content_response = document_service.get_document_content(document_id)
    chunks = content_response.data.chunks
    
    # Initialize VectorStoreService
    vector_store_service = VectorStoreService(document_repository=document_service.repository)
    
    # Index document (this will generate embeddings and save FAISS index)
    return vector_store_service.index_document(document_id, chunks)

@router.get("/status", response_model=VectorIndexStatusResponse, description="Check vector indexing status.")
def get_vector_index_status(document_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_repository = DocumentRepository(db, current_user.id)
    vector_store_service = VectorStoreService(document_repository)
    return vector_store_service.get_index_status(document_id)

@router.delete("", response_model=VectorIndexDeleteResponse, description="Delete FAISS index for a document.")
def delete_vector_index(document_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document_repository = DocumentRepository(db, current_user.id)
    vector_store_service = VectorStoreService(document_repository)
    
    vector_store_service.delete_document_index(document_id)
    
    return VectorIndexDeleteResponse(
        success=True,
        message="Vector index deleted successfully"
    )
