import logging
from uuid import UUID
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.services.upload_service import UploadService
from app.services.document_processing_service import DocumentProcessingService
from app.schemas.document import (
    DocumentMetadata, DocumentUploadResponse, DocumentUploadData,
    DocumentProcessingResponse, DocumentMetrics,
    DocumentContentResponse, DocumentContentData
)
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.upload_service = UploadService()
        self.processing_service = DocumentProcessingService()

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

    def process_document(self, document_id: UUID) -> DocumentProcessingResponse:
        logger.info(f"Document Processing API Started for ID: {document_id}")
        doc = self.repository.get_by_id(document_id)
        if not doc:
            raise AppError("Document Not Found", status_code=404)

        try:
            result = self.processing_service.process_document(doc.file_path)
            
            self.repository.mark_processed(document_id)
            
            logger.info(f"Document Processing API Completed for ID: {document_id}")
            return DocumentProcessingResponse(
                success=True,
                message="Document processed successfully",
                data=DocumentMetrics(
                    document_id=document_id,
                    character_count=result['character_count'],
                    word_count=result['word_count'],
                    chunk_count=result['chunk_count'],
                    average_chunk_size=result['average_chunk_size']
                )
            )
        except AppError:
            raise
        except Exception as e:
            logger.error(f"Processing Failure for document {document_id}: {e}", exc_info=True)
            raise AppError("Processing Failure.", status_code=500)

    def get_document_content(self, document_id: UUID) -> DocumentContentResponse:
        doc = self.repository.get_by_id(document_id)
        if not doc:
            raise AppError("Document Not Found", status_code=404)

        if not doc.processed:
            raise AppError("Document Not Processed. Please process the document first.", status_code=400)

        logger.info(f"Content Retrieval for Document ID: {document_id}")
        try:
            result = self.processing_service.process_document(doc.file_path)
            return DocumentContentResponse(
                success=True,
                data=DocumentContentData(
                    document_id=document_id,
                    processed=doc.processed,
                    character_count=result['character_count'],
                    word_count=result['word_count'],
                    chunk_count=result['chunk_count'],
                    chunks=result['chunks']
                )
            )
        except AppError:
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve content for document {document_id}: {e}", exc_info=True)
            raise AppError("Failed to retrieve document content.", status_code=500)
