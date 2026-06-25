import pytest
from app.services.ats_service import AtsService

def test_calculate_ats_score_perfect():
    service = AtsService()
    parsed_data = {
        "contact": {"name": "John", "email": "john@doe.com", "phone": "123"},
        "skills": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "projects": [{"name": "P1"}, {"name": "P2"}],
        "education": [{"degree": "BSc"}],
        "certifications": [{"name": "Cert1"}, {"name": "Cert2"}],
        "experience": [{"company": "A"}, {"company": "B"}]
    }
    
    score, breakdown, missing, improvements = service.calculate_ats_score(parsed_data)
    
    assert score == 100
    assert len(missing) == 0
    assert breakdown["Contact Info"] == 10
    assert breakdown["Skills"] == 20
    assert breakdown["Projects"] == 20
    assert breakdown["Education"] == 15
    assert breakdown["Certifications"] == 10
    assert breakdown["Keywords"] == 15
    assert breakdown["Formatting & Completeness"] == 10

def test_calculate_ats_score_empty():
    service = AtsService()
    score, breakdown, missing, improvements = service.calculate_ats_score({})
    
    assert score == 5 # Minimum formatting score
    assert "Contact Information" in missing
    assert "Skills" in missing
    assert "Projects" in missing
    assert "Education" in missing
    assert len(improvements) > 0
