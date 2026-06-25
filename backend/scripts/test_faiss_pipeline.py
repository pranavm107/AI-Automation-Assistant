import os
import sys
import time
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.embedding_service import EmbeddingService
from app.vector_store.faiss_manager import FaissManager

def run():
    print("=== FAISS Pipeline Verification ===")
    
    sample_path = "tests/fixtures/sample_notes.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Ensure you are in the backend directory and it exists.")
        return
        
    processing_service = DocumentProcessingService()
    embedding_service = EmbeddingService()
    faiss_manager = FaissManager()
    
    try:
        print("1. Extracting and chunking document...")
        result = processing_service.process_document(sample_path)
        chunks = result['chunks']
        print(f"   -> Extracted {len(chunks)} chunks.")
        
        print("2. Generating embeddings...")
        embeddings = embedding_service.generate_embeddings(chunks)
        expected_dim = embedding_service.get_embedding_dimension()
        
        print("3. Creating FAISS Index...")
        start_time = time.time()
        index = faiss_manager.create_index(dimension=expected_dim, embeddings=embeddings)
        
        print("4. Saving FAISS Index to disk...")
        doc_id = str(uuid4())
        path = faiss_manager.save_index(index, doc_id)
        
        print("5. Reloading FAISS Index from disk...")
        loaded_index = faiss_manager.load_index(doc_id)
        duration = time.time() - start_time
        
        print("\n--- Statistics ---")
        print(f"Document Name: {os.path.basename(sample_path)}")
        print(f"Vector Count: {faiss_manager.get_vector_count(loaded_index)}")
        print(f"Dimension: {expected_dim}")
        print(f"Index Path: {path}")
        print(f"Index Size: {os.path.getsize(path)} bytes")
        print(f"Execution Time (FAISS I/O): {duration:.4f} seconds")
        
        print("\n6. Cleaning up...")
        faiss_manager.delete_index(doc_id)
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
