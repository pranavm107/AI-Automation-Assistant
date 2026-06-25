import pytest
import os
import faiss
from uuid import uuid4
from app.vector_store.faiss_manager import FaissManager
from app.core.exceptions import AppError

def test_faiss_manager_lifecycle(tmp_path):
    manager = FaissManager(base_dir=str(tmp_path))
    doc_id = str(uuid4())
    dimension = 4
    embeddings = [
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8]
    ]
    
    # Test Create
    index = manager.create_index(dimension, embeddings)
    assert isinstance(index, faiss.IndexFlatL2)
    assert manager.get_vector_count(index) == 2
    
    # Test Save
    path = manager.save_index(index, doc_id)
    assert os.path.exists(path)
    assert manager.index_exists(doc_id)
    
    # Test Load
    loaded_index = manager.load_index(doc_id)
    assert isinstance(loaded_index, faiss.Index)
    assert manager.get_vector_count(loaded_index) == 2
    
    # Test Delete
    assert manager.delete_index(doc_id) is True
    assert not os.path.exists(path)
    assert not manager.index_exists(doc_id)

def test_faiss_manager_load_missing(tmp_path):
    manager = FaissManager(base_dir=str(tmp_path))
    with pytest.raises(AppError) as exc_info:
        manager.load_index(str(uuid4()))
    assert exc_info.value.status_code == 404
