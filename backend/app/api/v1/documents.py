from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.services.document_service import DocumentService
from app.schemas.document import DocumentUploadResponse, DocumentListResponse, DocumentDetailResponse, DocumentDeleteResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentUploadResponse, description="Upload a document and save metadata.")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    return await document_service.upload_document(file)

@router.get("", response_model=DocumentListResponse, description="Retrieve all uploaded documents.")
def get_documents(db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    docs = document_service.get_documents()
    return DocumentListResponse(success=True, data=docs)

@router.get("/{document_id}", response_model=DocumentDetailResponse, description="Retrieve metadata for a single document.")
def get_document_details(document_id: UUID, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    doc = document_service.get_document_by_id(document_id)
    return DocumentDetailResponse(success=True, data=doc)

@router.delete("/{document_id}", response_model=DocumentDeleteResponse, description="Delete document and metadata.")
def delete_document(document_id: UUID, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    document_service.delete_document(document_id)
    return DocumentDeleteResponse(success=True, message="Document deleted successfully")
