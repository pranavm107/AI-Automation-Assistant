import os
import sys
import time
from uuid import uuid4
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_processing_service import DocumentProcessingService
from app.services.job_matching_service import JobMatchingService
from app.services.job_recommendation_service import JobRecommendationService
from app.services.career_roadmap_service import CareerRoadmapService

def run():
    print("=== AI Job Intelligence Engine ===")
    
    sample_path = "tests/fixtures/sample_resume.txt"
    if not os.path.exists(sample_path):
        print(f"Fixture {sample_path} not found. Creating a temporary one for testing...")
        os.makedirs(os.path.dirname(sample_path), exist_ok=True)
        with open(sample_path, 'w') as f:
            f.write("""
John Doe
john.doe@example.com | 555-0100

Skills:
Python, FastAPI, Docker, Kubernetes, SQL

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
    
    mock_doc_service = MagicMock()
    mock_content = MagicMock()
    mock_content.data.chunks = result['chunks']
    mock_doc_service.get_document_content.return_value = mock_content
    
    match_service = JobMatchingService(mock_doc_service)
    rec_service = JobRecommendationService(mock_doc_service)
    roadmap_service = CareerRoadmapService(mock_doc_service)
    
    mock_jd = """
    Looking for a Backend Developer.
    Required: Python, AWS, Docker, GraphQL.
    Preferred: Kubernetes.
    Education: BS in Computer Science.
    """
    
    try:
        start_time = time.time()
        
        print("\n[Action] 1. Matching Resume to Job Description...")
        match_data = match_service.match_resume_to_job(doc_id, mock_jd)
        
        print("\n[Action] 2. Generating Role Recommendations...")
        recs = rec_service.recommend_jobs(doc_id)
        
        print("\n[Action] 3. Generating Career Roadmap for 'Machine Learning Engineer'...")
        roadmap = roadmap_service.generate_roadmap(doc_id, "Machine Learning Engineer")
        
        duration = time.time() - start_time
        
        print("\n" + "="*50)
        print("JOB INTELLIGENCE REPORT")
        print("="*50)
        
        print(f"\n--- MATCH SCORE: {match_data['match_score']}/100 ---")
        print(f"Matching Skills: {match_data['matching_skills']}")
        print(f"Missing Skills: {match_data['missing_skills']}")
        print("Recommendations:")
        for r in match_data['recommendations']:
            print(f"  - {r}")
            
        print("\n--- RECOMMENDED ROLES ---")
        for rec in recs:
            print(f"Role: {rec['role']} (Match: {rec['match']}%) - {rec['reason']}")
            
        print("\n--- CAREER ROADMAP (Target: ML Engineer) ---")
        print(f"Core Skills to Learn: {roadmap['recommended_skills']}")
        for m in roadmap['milestones']:
            print(f"{m['month']} - {m['focus']}: {m['topics']}")
            
        print(f"\nExecution Time: {duration:.4f} seconds")
        print("Pipeline executed successfully!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()
