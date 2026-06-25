import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String, nullable=False, unique=True)
    original_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    upload_status = Column(String, nullable=False, default='uploaded')
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime, nullable=True)
    embeddings_generated = Column(Boolean, default=False)
    embeddings_generated_at = Column(DateTime, nullable=True)
    embedding_model = Column(String(100), nullable=True)
    embedding_dimension = Column(Integer, nullable=True)
    vector_indexed = Column(Boolean, default=False)
    vector_indexed_at = Column(DateTime, nullable=True)
    faiss_document_id = Column(String(255), nullable=True)
    vector_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
