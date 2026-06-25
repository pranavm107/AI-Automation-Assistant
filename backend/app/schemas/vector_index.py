from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class VectorIndexData(BaseModel):
    document_id: UUID
    faiss_document_id: str
    vector_count: int
    embedding_dimension: int
    index_type: str

class VectorIndexResponse(BaseModel):
    success: bool
    message: str
    data: VectorIndexData

class VectorIndexStatusData(BaseModel):
    vector_indexed: bool
    vector_count: Optional[int] = None
    faiss_document_id: Optional[str] = None
    indexed_at: Optional[datetime] = None

class VectorIndexStatusResponse(BaseModel):
    success: bool
    data: VectorIndexStatusData

class VectorIndexDeleteResponse(BaseModel):
    success: bool
    message: str
