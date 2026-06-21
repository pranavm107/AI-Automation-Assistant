from sqlalchemy.orm import Session
from app.models.document import Document
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: UUID) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_all(self) -> List[Document]:
        return self.db.query(Document).order_by(Document.created_at.desc()).all()

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
