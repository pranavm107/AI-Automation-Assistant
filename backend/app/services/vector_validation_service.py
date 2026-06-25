import math
import logging
from typing import List
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

class VectorValidationService:
    @staticmethod
    def validate_embeddings(embeddings: List[List[float]], expected_dim: int) -> None:
        """
        Validates the generated embeddings for:
        - Non-empty
        - Consistent dimensions matching expected_dim
        - No NaN values
        - No infinite values
        """
        if not embeddings:
            raise AppError("Validation Failure: Embeddings list is empty.", status_code=500)

        for i, vector in enumerate(embeddings):
            if not isinstance(vector, list):
                raise AppError(f"Validation Failure: Vector at index {i} is not a list.", status_code=500)
                
            if len(vector) != expected_dim:
                raise AppError(f"Validation Failure: Vector at index {i} has dimension {len(vector)}, expected {expected_dim}.", status_code=500)
            
            for j, val in enumerate(vector):
                if not isinstance(val, (int, float)):
                    raise AppError(f"Validation Failure: Value at vector {i}, dimension {j} is not a number.", status_code=500)
                if math.isnan(val):
                    raise AppError(f"Validation Failure: NaN value detected at vector {i}, dimension {j}.", status_code=500)
                if math.isinf(val):
                    raise AppError(f"Validation Failure: Infinite value detected at vector {i}, dimension {j}.", status_code=500)
                    
        logger.info("Vector validation passed successfully.")
