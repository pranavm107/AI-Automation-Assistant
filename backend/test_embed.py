import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.embedding_service import EmbeddingService

try:
    svc = EmbeddingService()
    svc.generate_embeddings(["Test text"])
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
