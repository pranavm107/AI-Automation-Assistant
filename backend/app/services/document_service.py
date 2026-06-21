import logging
from uuid import UUID
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.services.upload_service import UploadService
from app.schemas.document import DocumentMetadata, DocumentUploadResponse, DocumentUploadData
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.upload_service = UploadService()

    async def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        logger.info(f"Upload start for file: {file.filename}")
        
        safe_filename, original_name, size, file_type = await self.upload_service.upload_file(file)
        
        try:
            document = Document(
                file_name=safe_filename,
                original_name=original_name,
                file_type=file_type,
                file_size=size,
                file_path=f"uploads/{safe_filename}",
                upload_status="uploaded"
            )
            saved_doc = self.repository.create(document)
            logger.info(f"Upload success for document ID: {saved_doc.id}")
            
            return DocumentUploadResponse(
                success=True,
                message="Document uploaded successfully",
                data=DocumentUploadData(
                    document_id=saved_doc.id,
                    file_name=original_name
                )
            )
        except Exception as e:
            logger.error(f"Database operation failed during upload: {e}", exc_info=True)
            self.upload_service.delete_file(safe_filename)
            raise AppError("Database failure while saving document metadata.", status_code=500)

    def get_documents(self) -> List[DocumentMetadata]:
        try:
            docs = self.repository.get_all()
            return [DocumentMetadata.model_validate(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            raise AppError("Database failure.", status_code=500)

    def get_document_by_id(self, document_id: UUID) -> DocumentMetadata:
        doc = self.repository.get_by_id(document_id)
        if not doc:
            raise AppError("Document Not Found", status_code=404)
        return DocumentMetadata.model_validate(doc)

    def delete_document(self, document_id: UUID) -> None:
        doc = self.repository.get_by_id(document_id)
        if not doc:
            raise AppError("Document Not Found", status_code=404)
        
        self.upload_service.delete_file(doc.file_name)
        
        try:
            self.repository.delete(doc)
            logger.info(f"Document {document_id} metadata deleted.")
        except Exception as e:
            logger.error(f"Failed to delete document metadata {document_id}: {e}")
            raise AppError("Database failure.", status_code=500)
