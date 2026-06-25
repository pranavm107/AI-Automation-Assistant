import logging
from typing import List, Dict, Any, Tuple
from app.core.exceptions import AppError
from app.services.retrieval_service import RetrievalService
from app.services.gemini_service import GeminiService
from app.repositories.document_repository import DocumentRepository

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self, document_repository: DocumentRepository = None):
        self.retrieval_service = RetrievalService()
        self.gemini_service = GeminiService()
        self.document_repository = document_repository

    def _build_prompt(self, question: str, chunks: List[str]) -> str:
        """Constructs the strict RAG prompt."""
        context = "\n\n---\n\n".join(chunks)
        
        prompt = f"""You are an AI document assistant.
Answer only using the provided context.
If the answer is not found in the context, respond:
"The document does not contain enough information to answer this question."

Context:
{context}

Question:
{question}

Answer:"""
        return prompt

    def _format_sources(self, matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formats the raw matches into SourceReferences."""
        sources = []
        for match in matches:
            sources.append({
                "chunk_id": match['chunk_id'],
                "score": match['score'],
                "document_id": match.get('document_id')
            })
        return sources

    def ask_document(self, document_id: str, question: str) -> Tuple[str, float, List[Dict[str, Any]]]:
        """
        Asks a question against a single document.
        Returns: Answer, Max Confidence Score, Sources
        """
        logger.info(f"RAG: Asking question against document {document_id}")
        
        # 1. Retrieve
        matches = self.retrieval_service.search_document(document_id, question, top_k=5)
        
        if not matches:
            raise AppError("No relevant context found in document.", status_code=404)
            
        # 2. Extract context
        chunks = [match['chunk'] for match in matches]
        
        # 3. Build Prompt
        prompt = self._build_prompt(question, chunks)
        
        # 4. Generate Answer
        logger.info("RAG: Sending assembled prompt to Gemini.")
        answer = self.gemini_service.generate_response(prompt)
        
        # 5. Calculate overall confidence (highest retrieved score)
        confidence = max(match['score'] for match in matches) if matches else 0.0
        
        # 6. Format sources
        sources = self._format_sources(matches)
        
        return answer, confidence, sources

    def ask_global(self, question: str) -> Tuple[str, float, List[Dict[str, Any]]]:
        """
        Asks a question globally across all indexed documents.
        """
        logger.info("RAG: Asking question globally.")
        
        if not self.document_repository:
            raise AppError("DocumentRepository not provided for global search.", status_code=500)
            
        # Get all indexed documents
        all_docs = self.document_repository.get_all()
        indexed_doc_ids = [str(doc.id) for doc in all_docs if doc.vector_indexed]
        
        if not indexed_doc_ids:
            raise AppError("No indexed documents available for global search.", status_code=404)
            
        # 1. Retrieve globally
        matches = self.retrieval_service.search_top_k(indexed_doc_ids, question, top_k=10) # Maybe slightly more context globally
        
        if not matches:
            raise AppError("No relevant context found in any documents.", status_code=404)
            
        # 2. Extract context
        chunks = [match['chunk'] for match in matches]
        
        # 3. Build Prompt
        prompt = self._build_prompt(question, chunks)
        
        # 4. Generate Answer
        logger.info("RAG: Sending assembled prompt to Gemini.")
        answer = self.gemini_service.generate_response(prompt)
        
        # 5. Calculate overall confidence
        confidence = max(match['score'] for match in matches) if matches else 0.0
        
        # 6. Format sources
        sources = self._format_sources(matches)
        
        return answer, confidence, sources
