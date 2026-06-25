import pytest
from unittest.mock import MagicMock, patch
from app.services.rag_service import RagService
from app.core.exceptions import AppError

def test_ask_document_success():
    with patch('app.services.rag_service.RetrievalService') as MockRetrieval:
        with patch('app.services.rag_service.GeminiService') as MockGemini:
            mock_retrieval = MockRetrieval.return_value
            mock_retrieval.search_document.return_value = [
                {"chunk": "chunk 1", "score": 0.9, "chunk_id": 0, "document_id": "doc1"}
            ]
            
            mock_gemini = MockGemini.return_value
            mock_gemini.generate_response.return_value = "This is the answer."
            
            service = RagService()
            answer, confidence, sources = service.ask_document("doc1", "question")
            
            assert answer == "This is the answer."
            assert confidence == 0.9
            assert len(sources) == 1
            assert sources[0]['chunk_id'] == 0

def test_ask_document_no_context():
    with patch('app.services.rag_service.RetrievalService') as MockRetrieval:
        mock_retrieval = MockRetrieval.return_value
        mock_retrieval.search_document.return_value = []
        
        service = RagService()
        with pytest.raises(AppError) as exc_info:
            service.ask_document("doc1", "question")
        assert exc_info.value.status_code == 404

def test_ask_global_success():
    with patch('app.services.rag_service.RetrievalService') as MockRetrieval:
        with patch('app.services.rag_service.GeminiService') as MockGemini:
            mock_repo = MagicMock()
            mock_doc = MagicMock()
            mock_doc.id = "doc1"
            mock_doc.vector_indexed = True
            mock_repo.get_all.return_value = [mock_doc]
            
            mock_retrieval = MockRetrieval.return_value
            mock_retrieval.search_top_k.return_value = [
                {"chunk": "chunk 1", "score": 0.8, "chunk_id": 0, "document_id": "doc1"}
            ]
            
            mock_gemini = MockGemini.return_value
            mock_gemini.generate_response.return_value = "Global answer."
            
            service = RagService(document_repository=mock_repo)
            answer, confidence, sources = service.ask_global("question")
            
            assert answer == "Global answer."
            assert confidence == 0.8
            mock_retrieval.search_top_k.assert_called_once_with(["doc1"], "question", top_k=10)
