# API Documentation

Base URL

[http://localhost:8000/api/v1](http://localhost:8000/api/v1)

---

## Documents

POST /documents/upload

Upload a document.

GET /documents

Retrieve all documents.

DELETE /documents/{document_id}

Delete a document.

POST /documents/{document_id}/process

Process uploaded document.

GET /documents/{document_id}/content

Retrieve processed content.

---

## Embeddings

POST /documents/{document_id}/embeddings

Generate embeddings.

GET /documents/{document_id}/embeddings/status

Get embedding status.

---

## Vector Index

POST /documents/{document_id}/index

Create FAISS index.

GET /documents/{document_id}/index/status

Get index status.

DELETE /documents/{document_id}/index

Delete FAISS index.

---

## RAG

POST /documents/{document_id}/ask

Ask questions against a document.

POST /chat/rag

Global RAG search.

GET /documents/{document_id}/search

Debug retrieval endpoint.

---

## Resume

POST /resume/analyze

Analyze resume.

POST /resume/ats-score

Generate ATS score.

POST /resume/skill-gap

Generate skill gap analysis.

GET /resume/health

Health endpoint.

---

## Interview

POST /interview/generate

Generate interview questions.

POST /interview/project-based

Generate project-based questions.

POST /interview/hr

Generate HR questions.

POST /interview/mock

Generate complete mock interview.

GET /interview/health

Health endpoint.

---

## Job Intelligence

POST /job/match

Match resume against JD.

POST /job/recommend

Recommend jobs.

POST /job/roadmap

Generate roadmap.

POST /job/compare

Compare resume and JD.

GET /job/health

Health endpoint.
