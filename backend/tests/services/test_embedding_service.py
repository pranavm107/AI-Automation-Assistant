import pytest
import math
from app.services.embedding_service import EmbeddingService
from app.services.vector_validation_service import VectorValidationService
from app.core.exceptions import AppError

def test_generate_embeddings_valid():
    service = EmbeddingService()
    chunks = ["This is a test chunk.", "Another test chunk here."]
    
    embeddings = service.generate_embeddings(chunks)
    
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384
    
    # Validation should pass
    VectorValidationService.validate_embeddings(embeddings, 384)

def test_generate_embeddings_empty():
    service = EmbeddingService()
    with pytest.raises(AppError) as exc_info:
        service.generate_embeddings([])
    assert "Empty Chunks provided" in str(exc_info.value)
    assert exc_info.value.status_code == 400

def test_vector_validation_failure_empty():
    with pytest.raises(AppError) as exc_info:
        VectorValidationService.validate_embeddings([], 384)
    assert "Embeddings list is empty" in str(exc_info.value)

def test_vector_validation_failure_dimension():
    embeddings = [[0.1] * 383] # Missing one dimension
    with pytest.raises(AppError) as exc_info:
        VectorValidationService.validate_embeddings(embeddings, 384)
    assert "has dimension 383, expected 384" in str(exc_info.value)

def test_vector_validation_failure_nan():
    embeddings = [[0.1] * 383 + [math.nan]]
    with pytest.raises(AppError) as exc_info:
        VectorValidationService.validate_embeddings(embeddings, 384)
    assert "NaN value detected" in str(exc_info.value)
