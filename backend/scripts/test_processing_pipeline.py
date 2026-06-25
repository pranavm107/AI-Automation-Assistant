import os
import sys
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService

def run():
    print("=== Document Processing Pipeline Verification ===")
    
    sample_path = "tests/fixtures/sample_notes.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Run generate_fixtures.py first.")
        return
        
    service = DocumentProcessingService()
    try:
        # Mocking API flow logic for console printout
        document_id = str(uuid4())
        print(f"Document ID: {document_id}")
        print("Processing Status: Processing Started...")
        
        result = service.process_document(sample_path)
        
        print("Processing Status: Completed")
        print("\n--- Metrics ---")
        print(f"Character Count: {result['character_count']}")
        print(f"Word Count: {result['word_count']}")
        print(f"Chunk Count: {result['chunk_count']}")
        print(f"Average Chunk Size: {result['average_chunk_size']}")
        
        print("\n--- Preview First Chunk (Content API Simulation) ---")
        if result['chunks']:
            print(result['chunks'][0])
        else:
            print("No chunks generated.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
