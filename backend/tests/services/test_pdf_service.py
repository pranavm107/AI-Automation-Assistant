import pytest
from unittest.mock import patch
from app.services.pdf_service import PDFService
from app.core.exceptions import PDFExtractionError

@patch('os.path.exists', return_value=False)
def test_pdf_missing(mock_exists):
    service = PDFService()
    with pytest.raises(PDFExtractionError):
        service.extract_text("missing.pdf")
