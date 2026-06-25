from app.services.chunking_service import ChunkingService

def test_chunking_basic():
    service = ChunkingService(chunk_size=10, overlap=2)
    text = "1234567890abcdefghij"
    chunks = service.chunk_text(text)
    assert len(chunks) > 1
    assert chunks[0] == "1234567890"

def test_chunking_empty():
    service = ChunkingService()
    chunks = service.chunk_text("")
    assert len(chunks) == 0
