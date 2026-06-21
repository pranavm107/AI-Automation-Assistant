# AI Automation Assistant - API Map

## API Overview

This document defines all backend API endpoints exposed by the AI Automation Assistant.

Purpose:

* API standardization
* Frontend integration guidance
* Service mapping
* Request/Response contracts
* Future scalability planning

Base URL:

/api

Version:

v1

Full Base Path:

/api/v1

---

# API Architecture

Frontend
↓
API Route
↓
Validation
↓
Workflow / Service
↓
Database / FAISS / Gemini
↓
Response

---

# Response Standards

## Success Response

{
"success": true,
"message": "Operation completed successfully",
"data": {}
}

---

## Error Response

{
"success": false,
"message": "Operation failed",
"errors": []
}

---

# Health APIs

## Health Check

Method:

GET

Route:

/api/v1/health

Purpose:

Verify backend availability.

Response:

{
"success": true,
"message": "Server is running"
}

---

# Chat APIs

## Generate AI Response

Method:

POST

Route:

/api/v1/chat

Purpose:

Handle conversational AI requests.

Services:

* Chat Service
* Gemini Service

Request:

{
"message": "Explain Machine Learning"
}

Validation:

* Required
* Non-empty string
* Maximum 5000 characters

Response:

{
"success": true,
"data": {
"answer": "Machine Learning is..."
}
}

---

# Document Upload APIs

## Upload Document

Method:

POST

Route:

/api/v1/documents/upload

Purpose:

Upload documents for processing.

Services:

* Upload Service
* PDF Service
* Embedding Service
* Vector Service

Request:

multipart/form-data

Fields:

file

Supported Types:

* PDF
* DOCX
* TXT

Maximum Size:

20 MB

Response:

{
"success": true,
"data": {
"document_id": "uuid",
"filename": "resume.pdf"
}
}

---

## Get Uploaded Documents

Method:

GET

Route:

/api/v1/documents

Purpose:

Retrieve uploaded documents.

Response:

{
"success": true,
"data": []
}

---

## Get Document Details

Method:

GET

Route:

/api/v1/documents/{document_id}

Purpose:

Retrieve document metadata.

Response:

{
"success": true,
"data": {}
}

---

## Delete Document

Method:

DELETE

Route:

/api/v1/documents/{document_id}

Purpose:

Delete uploaded document.

Response:

{
"success": true,
"message": "Document deleted"
}

---

# RAG APIs

## Document Question Answering

Method:

POST

Route:

/api/v1/rag/query

Purpose:

Answer questions using uploaded documents.

Services:

* Embedding Service
* Vector Service
* Gemini Service

Request:

{
"document_id": "uuid",
"question": "What skills are mentioned?"
}

Response:

{
"success": true,
"data": {
"answer": "...",
"sources": []
}
}

---

## Search Document Context

Method:

POST

Route:

/api/v1/rag/search

Purpose:

Retrieve relevant document chunks.

Request:

{
"document_id": "uuid",
"query": "Python experience"
}

Response:

{
"success": true,
"data": {
"chunks": []
}
}

---

# Resume Analysis APIs

## Analyze Resume

Method:

POST

Route:

/api/v1/resume/analyze

Purpose:

Generate resume insights.

Services:

* Resume Workflow
* Gemini Service

Request:

{
"document_id": "uuid"
}

Response:

{
"success": true,
"data": {
"candidate_summary": "",
"skills": [],
"strengths": [],
"recommendations": []
}
}

---

## ATS Analysis

Method:

POST

Route:

/api/v1/resume/ats-analysis

Purpose:

Evaluate ATS readiness.

Response:

{
"success": true,
"data": {
"score": 85,
"improvements": []
}
}

---

# Interview Generator APIs

## Generate Interview Questions

Method:

POST

Route:

/api/v1/interview/generate

Purpose:

Generate interview questions.

Services:

* Interview Workflow
* Gemini Service

Request:

{
"document_id": "uuid"
}

Response:

{
"success": true,
"data": {
"hr_questions": [],
"technical_questions": [],
"project_questions": [],
"behavioral_questions": []
}
}

---

# Document Summary APIs

## Generate Summary

Method:

POST

Route:

/api/v1/summary/generate

Purpose:

Generate document summary.

Services:

* Summary Workflow
* Gemini Service

Request:

{
"document_id": "uuid"
}

Response:

{
"success": true,
"data": {
"summary": "",
"key_points": [],
"conclusion": ""
}
}

---

# Workflow APIs

## Execute Workflow

Method:

POST

Route:

/api/v1/workflows/execute

Purpose:

Execute predefined workflow.

Request:

{
"workflow_name": "resume_analysis",
"document_id": "uuid"
}

Response:

{
"success": true,
"data": {}
}

---

## Get Available Workflows

Method:

GET

Route:

/api/v1/workflows

Purpose:

Retrieve supported workflows.

Response:

{
"success": true,
"data": [
"resume_analysis",
"interview_generation",
"document_summary"
]
}

---

# Chat History APIs

## Get Chat History

Method:

GET

Route:

/api/v1/chat/history

Purpose:

Retrieve conversation history.

Response:

{
"success": true,
"data": []
}

---

## Delete Chat History

Method:

DELETE

Route:

/api/v1/chat/history

Purpose:

Clear conversation history.

Response:

{
"success": true,
"message": "History cleared"
}

---

# Analytics APIs (Future)

## Dashboard Metrics

Method:

GET

Route:

/api/v1/analytics/dashboard

Purpose:

Retrieve application metrics.

Response:

{
"success": true,
"data": {}
}

---

# Authentication APIs (Future)

## Register User

POST

/api/v1/auth/register

---

## Login User

POST

/api/v1/auth/login

---

## Logout User

POST

/api/v1/auth/logout

---

## Refresh Token

POST

/api/v1/auth/refresh

---

# Service Mapping

Chat API
→ Chat Service
→ Gemini Service

Upload API
→ Upload Service
→ PDF Service
→ Embedding Service
→ Vector Service

Resume API
→ Resume Workflow
→ Gemini Service

Interview API
→ Interview Workflow
→ Gemini Service

Summary API
→ Summary Workflow
→ Gemini Service

RAG API
→ Embedding Service
→ Vector Service
→ Gemini Service

---

# Validation Rules

All APIs must:

* Validate input
* Validate file types
* Validate file size
* Return standardized responses
* Handle exceptions gracefully
* Log failures

---

# Security Requirements

All APIs must:

* Validate requests
* Sanitize inputs
* Protect secrets
* Prevent prompt injection where possible
* Restrict file uploads
* Enforce rate limiting (future)

---

# Future APIs

Phase 2

* User Profiles
* Document Collections
* Saved Reports

Phase 3

* Workflow Builder
* Agent Management
* Team Collaboration

Phase 4

* Voice Assistant
* Real-Time Notifications
* AI Memory APIs

---

# API Design Rules

1. Controllers remain thin.
2. Business logic belongs in services.
3. Multi-step logic belongs in workflows.
4. APIs must remain versioned.
5. Breaking changes require version updates.
6. Response format must remain consistent.
7. Validation must occur before service execution.
8. Every API must be documented before implementation.
