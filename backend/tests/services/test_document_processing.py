import pytest
from unittest.mock import patch, MagicMock
from app.services.document_processing_service import DocumentProcessingService
from app.core.exceptions import AppError

@patch('os.path.exists', return_value=True)
@patch('app.services.pdf_service.PDFService.extract_text', return_value="PDF text")
def test_process_pdf_success(mock_extract, mock_exists):
    service = DocumentProcessingService()
    result = service.process_document("test.pdf")
    assert "PDF text" in result['text']
    assert result['character_count'] == 8

@patch('os.path.exists', return_value=True)
def test_process_unsupported_file(mock_exists):
    service = DocumentProcessingService()
    with pytest.raises(AppError) as exc:
        service.process_document("test.mp4")
    assert exc.value.status_code == 400
