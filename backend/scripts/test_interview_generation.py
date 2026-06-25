import os
import sys
import time
from uuid import uuid4
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.mock_interview_service import MockInterviewService

def run():
    print("=== AI Mock Interview Generation ===")
    
    sample_path = "tests/fixtures/sample_resume.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Creating a temporary one for testing...")
        os.makedirs(os.path.dirname(sample_path), exist_ok=True)
        with open(sample_path, 'w') as f:
            f.write("""
John Doe
john.doe@example.com | 555-0100

Skills:
Python, FastAPI, Docker, Kubernetes, SQL, AWS

Education:
B.S. Computer Science, State University, 2020

Experience:
Backend Developer at TechCorp
- Built scalable APIs using Python and FastAPI.
- Containerized applications with Docker.
            """)
            
    doc_id = str(uuid4())
    
    # Simulate processing
    processing_service = DocumentProcessingService()
    result = processing_service.process_document(sample_path)
    
    # Mock DocumentService
    mock_doc_service = MagicMock()
    mock_content = MagicMock()
    mock_content.data.chunks = result['chunks']
    mock_doc_service.get_document_content.return_value = mock_content
    
    mock_service = MockInterviewService(mock_doc_service)
    
    try:
        target_role = "Senior Backend Engineer"
        print(f"\n[Action] 1. Generating Mock Interview Session for {target_role}...")
        start_time = time.time()
        
        mock_data = mock_service.create_mock_interview(doc_id, target_role)
        
        duration = time.time() - start_time
        
        print("\n" + "="*50)
        print("MOCK INTERVIEW SESSION")
        print("="*50)
        
        print(f"\n[INTERVIEWER]:\n{mock_data['introduction']}")
        
        print("\n--- QUESTIONS ---")
        for i, q in enumerate(mock_data['questions'], 1):
            print(f"\nQ{i} ({q['category']} - {q['difficulty']}): {q['question']}")
            print(f"Expected Answer: {q['expected_answer']}")
            print(f"Evaluation Criteria:")
            for c in q['evaluation_criteria']:
                print(f"  - {c}")
                
        print("\n--- PREPARATION TIPS ---")
        for t in mock_data['preparation_tips']:
            print(f"- {t}")
            
        print(f"\nExecution Time: {duration:.4f} seconds")
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
