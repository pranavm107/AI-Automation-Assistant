from sqlalchemy.orm import Session
from app.models.document import Document
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class DocumentRepository:
    def __init__(self, db: Session, owner_id: UUID):
        self.db = db
        self.owner_id = owner_id

    def create(self, document: Document) -> Document:
        document.owner_id = self.owner_id
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: UUID) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id, Document.owner_id == self.owner_id).first()

    def get_all(self) -> List[Document]:
        return self.db.query(Document).filter(Document.owner_id == self.owner_id).order_by(Document.created_at.desc()).all()

    def delete(self, document: Document) -> None:
        self.db.delete(document)
        self.db.commit()

    def mark_processed(self, document_id: UUID) -> Optional[Document]:
        document = self.get_by_id(document_id)
        if document:
            document.processed = True
            document.processed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(document)
        return document

    def mark_embeddings_generated(self, document_id: UUID, model: str, dimension: int) -> Optional[Document]:
        document = self.get_by_id(document_id)
        if document:
            document.embeddings_generated = True
            document.embeddings_generated_at = datetime.utcnow()
            document.embedding_model = model
            document.embedding_dimension = dimension
            self.db.commit()
            self.db.refresh(document)
        return document

    def mark_vector_indexed(self, document_id: UUID, faiss_id: str, count: int) -> Optional[Document]:
        document = self.get_by_id(document_id)
        if document:
            document.vector_indexed = True
            document.vector_indexed_at = datetime.utcnow()
            document.faiss_document_id = faiss_id
            document.vector_count = count
            self.db.commit()
            self.db.refresh(document)
        return document

    def unmark_vector_indexed(self, document_id: UUID) -> Optional[Document]:
        document = self.get_by_id(document_id)
        if document:
            document.vector_indexed = False
            document.vector_indexed_at = None
            document.faiss_document_id = None
            document.vector_count = None
            self.db.commit()
            self.db.refresh(document)
        return document
