# Known Issues and Limitations

## Current Limitations (v1.0.0)

### 1. LLM Rate Limits
- The system heavily relies on the Gemini API. Generating intensive requests (like a comprehensive Job Match + Career Roadmap simultaneously) may hit rate limits on free or lower-tier API accounts.

### 2. Large File Parsing
- Extremely large PDFs or PDFs consisting entirely of images (without OCR layers) will fail to extract text properly, leading to empty embeddings or failed ATS analysis.

### 3. Local FAISS Storage
- FAISS indexes are currently saved locally to disk (`backend/vector_store`). If the backend container is redeployed without a persistent volume, the vector data will be lost, although the PostgreSQL metadata will remain, causing a desync.

### 4. Single-Tenant Architecture
- The platform currently has no user authentication or isolation. Every document uploaded is visible to anyone accessing the dashboard. (This is scheduled to be addressed in Phase 11).

### 5. Concurrent Indexing
- Heavy concurrent requests to encode text into embeddings via `SentenceTransformers` on CPU may cause latency spikes. GPU acceleration is recommended for production scale.
