from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class DocumentUploadData(BaseModel):
    document_id: UUID
    file_name: str

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    data: DocumentUploadData

class DocumentMetadata(BaseModel):
    id: UUID
    file_name: str
    original_name: str
    file_type: str
    file_size: int
    upload_status: str
    processed: bool
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DocumentListResponse(BaseModel):
    success: bool
    data: List[DocumentMetadata]

class DocumentDetailResponse(BaseModel):
    success: bool
    data: DocumentMetadata

class DocumentDeleteResponse(BaseModel):
    success: bool
    message: str

class DocumentMetrics(BaseModel):
    document_id: UUID
    character_count: int
    word_count: int
    chunk_count: int
    average_chunk_size: int

class DocumentProcessingResponse(BaseModel):
    success: bool
    message: str
    data: DocumentMetrics

class DocumentContentData(BaseModel):
    document_id: UUID
    processed: bool
    character_count: int
    word_count: int
    chunk_count: int
    chunks: List[str]

class DocumentContentResponse(BaseModel):
    success: bool
    data: DocumentContentData
