import os
import sys
import time
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_validation_service import VectorValidationService

def run():
    print("=== Embedding Pipeline Verification ===")
    
    sample_path = "tests/fixtures/sample_notes.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Run generate_fixtures.py first.")
        return
        
    processing_service = DocumentProcessingService()
    embedding_service = EmbeddingService()
    
    try:
        # Mocking API flow logic
        print("1. Extracting and chunking document...")
        result = processing_service.process_document(sample_path)
        chunks = result['chunks']
        print(f"   -> Extracted {len(chunks)} chunks.")
        
        print("2. Generating embeddings (This will load the model first time)...")
        start_time = time.time()
        embeddings = embedding_service.generate_embeddings(chunks)
        duration = time.time() - start_time
        
        print("3. Validating vectors...")
        expected_dim = embedding_service.get_embedding_dimension()
        VectorValidationService.validate_embeddings(embeddings, expected_dim)
        
        print("\n--- Statistics ---")
        print(f"Document Name: {os.path.basename(sample_path)}")
        print(f"Chunk Count: {len(chunks)}")
        print(f"Vector Count: {len(embeddings)}")
        print(f"Vector Dimension: {expected_dim}")
        print(f"Model Used: {embedding_service.get_model_name()}")
        print(f"Generation Time: {duration:.4f} seconds")
        
        print("\nPipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
