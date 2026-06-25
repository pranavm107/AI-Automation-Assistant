from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class EmbeddingGenerationData(BaseModel):
    document_id: UUID
    embedding_model: str
    embedding_dimension: int
    chunk_count: int
    vector_count: int

class EmbeddingGenerationResponse(BaseModel):
    success: bool
    message: str
    data: EmbeddingGenerationData

class EmbeddingStatusData(BaseModel):
    embeddings_generated: bool
    embedding_model: Optional[str] = None
    embedding_dimension: Optional[int] = None
    generated_at: Optional[datetime] = None

class EmbeddingStatusResponse(BaseModel):
    success: bool
    data: EmbeddingStatusData
