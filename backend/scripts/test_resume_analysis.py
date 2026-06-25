import os
import sys
import time
from uuid import uuid4
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.resume_analyzer_service import ResumeAnalyzerService
from app.services.document_service import DocumentService

def run():
    print("=== Resume Analysis Verification ===")
    
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
    
    # Process Document (simulate processing)
    processing_service = DocumentProcessingService()
    result = processing_service.process_document(sample_path)
    
    # Mock DocumentService to return the chunks
    mock_doc_service = MagicMock()
    mock_content = MagicMock()
    mock_content.data.chunks = result['chunks']
    mock_doc_service.get_document_content.return_value = mock_content
    
    analyzer_service = ResumeAnalyzerService(mock_doc_service)
    
    try:
        print("\n[Action] 1. Parsing and Analyzing Resume...")
        start_time = time.time()
        
        analysis = analyzer_service.analyze_resume(doc_id)
        ats = analyzer_service.get_ats_score(doc_id)
        
        print("\n[Action] 2. Performing Skill Gap Analysis (Target: Senior AI Engineer)...")
        gap = analyzer_service.analyze_skill_gap(doc_id, "Senior AI Engineer")
        
        duration = time.time() - start_time
        
        print("\n=== Resume Report ===")
        print(f"Name: {analyzer_service.parser_service.extract_name(analyzer_service.parser_service.parse_resume(doc_id))}")
        print(f"ATS Score: {ats['ats_score']}/100")
        print(f"Summary: {analysis['summary']}")
        print(f"\nStrengths: {analysis['strengths']}")
        print(f"Weaknesses: {analysis['weaknesses']}")
        print(f"Recommendations: {analysis['recommendations']}")
        
        print(f"\nSkill Gap (Target: Senior AI Engineer)")
        print(f"Missing Skills: {gap['missing_skills']}")
        print(f"Recommendations: {gap['recommended_skills']}")
        
        print(f"\nExecution Time: {duration:.4f} seconds")
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
