import os
import sys
import time
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.embedding_service import EmbeddingService
from app.vector_store.faiss_manager import FaissManager
from app.services.rag_service import RagService

def run():
    print("=== RAG Pipeline Verification ===")
    
    sample_path = "tests/fixtures/sample_notes.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Run generate_fixtures.py first.")
        return
        
    processing_service = DocumentProcessingService()
    embedding_service = EmbeddingService()
    faiss_manager = FaissManager()
    rag_service = RagService()
    
    doc_id = str(uuid4())
    
    try:
        print("\n[Setup] 1. Extracting and chunking document...")
        result = processing_service.process_document(sample_path)
        chunks = result['chunks']
        
        print("[Setup] 2. Generating embeddings...")
        embeddings = embedding_service.generate_embeddings(chunks)
        expected_dim = embedding_service.get_embedding_dimension()
        
        print("[Setup] 3. Creating and saving FAISS Index & Metadata...")
        index = faiss_manager.create_index(dimension=expected_dim, embeddings=embeddings)
        faiss_manager.save_index(index, doc_id)
        faiss_manager.save_chunk_metadata(doc_id, chunks)
        
        print("\n[RAG Action] Asking Question: 'What is this document about?'")
        start_time = time.time()
        
        answer, confidence, sources = rag_service.ask_document(doc_id, "What is this document about?")
        
        duration = time.time() - start_time
        
        print("\n--- Output ---")
        print(f"Answer: {answer}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Sources Retrieved: {len(sources)}")
        print(f"Execution Time: {duration:.4f} seconds")
        
        print("\n[Cleanup] Removing Index & Metadata...")
        faiss_manager.delete_index(doc_id)
        faiss_manager.delete_chunk_metadata(doc_id)
        
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
