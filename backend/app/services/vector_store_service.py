import logging
from uuid import UUID
from app.core.exceptions import AppError
from app.services.embedding_service import EmbeddingService
from app.services.vector_validation_service import VectorValidationService
from app.vector_store.faiss_manager import FaissManager
from app.repositories.document_repository import DocumentRepository
from app.schemas.vector_index import VectorIndexResponse, VectorIndexData, VectorIndexStatusResponse, VectorIndexStatusData

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self, document_repository: DocumentRepository):
        self.repository = document_repository
        self.faiss_manager = FaissManager()
        self.embedding_service = EmbeddingService()

    def index_document(self, document_id: UUID, chunks: list[str]) -> VectorIndexResponse:
        logger.info(f"Starting Vector Indexing for document: {document_id}")
        
        doc_id_str = str(document_id)
        
        if self.faiss_manager.index_exists(doc_id_str):
            raise AppError("Index Already Exists for this document.", status_code=400)
            
        if not chunks:
            raise AppError("Empty chunks provided. Cannot index.", status_code=400)

        # 1. Generate Embeddings
        embeddings = self.embedding_service.generate_embeddings(chunks)
        expected_dim = self.embedding_service.get_embedding_dimension()
        
        # 2. Validate Embeddings
        VectorValidationService.validate_embeddings(embeddings, expected_dim)
        
        # 3. Create FAISS Index
        index = self.faiss_manager.create_index(dimension=expected_dim, embeddings=embeddings)
        vector_count = self.faiss_manager.get_vector_count(index)
        
        # 4. Save Index and Metadata
        self.faiss_manager.save_index(index, doc_id_str)
        self.faiss_manager.save_chunk_metadata(doc_id_str, chunks)
        
        # 5. Update DB
        self.repository.mark_vector_indexed(document_id, faiss_id=doc_id_str, count=vector_count)
        
        return VectorIndexResponse(
            success=True,
            message="Document indexed successfully",
            data=VectorIndexData(
                document_id=document_id,
                faiss_document_id=doc_id_str,
                vector_count=vector_count,
                embedding_dimension=expected_dim,
                index_type="IndexFlatL2"
            )
        )

    def delete_document_index(self, document_id: UUID) -> None:
        logger.info(f"Deleting Vector Index for document: {document_id}")
        doc_id_str = str(document_id)
        
        if not self.faiss_manager.index_exists(doc_id_str):
            raise AppError("Index Missing", status_code=404)
            
        self.faiss_manager.delete_index(doc_id_str)
        self.faiss_manager.delete_chunk_metadata(doc_id_str)
        self.repository.unmark_vector_indexed(document_id)

    def get_index_status(self, document_id: UUID) -> VectorIndexStatusResponse:
        doc = self.repository.get_by_id(document_id)
        if not doc:
            raise AppError("Document Not Found", status_code=404)
            
        return VectorIndexStatusResponse(
            success=True,
            data=VectorIndexStatusData(
                vector_indexed=doc.vector_indexed,
                vector_count=doc.vector_count,
                faiss_document_id=doc.faiss_document_id,
                indexed_at=doc.vector_indexed_at
            )
        )
