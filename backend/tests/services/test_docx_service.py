import pytest
from unittest.mock import patch
from app.services.docx_service import DOCXService
from app.core.exceptions import DOCXExtractionError

@patch('os.path.exists', return_value=False)
def test_docx_missing(mock_exists):
    service = DOCXService()
    with pytest.raises(DOCXExtractionError):
        service.extract_text("missing.docx")
