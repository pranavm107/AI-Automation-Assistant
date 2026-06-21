# AI Automation Assistant - System Architecture

## Architecture Overview

AI Automation Assistant follows a modular, service-oriented architecture designed for scalability, maintainability, and separation of concerns.

The system consists of five primary layers:

1. Presentation Layer (Frontend)
2. API Layer (FastAPI)
3. Business Logic Layer
4. AI & RAG Layer
5. Data Layer

The architecture ensures that each layer has a single responsibility and communicates only through well-defined interfaces.

---

# High-Level System Architecture

User
↓
Frontend (React)
↓
FastAPI API Layer
↓
Business Services
↓
AI Services / Workflow Engine
↓
FAISS + PostgreSQL
↓
Response

---

# Core Architectural Principles

## Separation of Concerns

Every component should have a single responsibility.

Examples:

Frontend:
Responsible only for user interaction.

API Layer:
Responsible only for request handling.

Services:
Responsible for business logic.

Workflow Engine:
Responsible for orchestrating multiple services.

Database:
Responsible only for persistence.

---

## Thin Controllers

API routes should never contain business logic.

Incorrect:

Route
→ AI Call
→ Database Query
→ File Processing

Correct:

Route
→ Service
→ Response

---

## Service-Based Architecture

All reusable logic must be placed inside services.

Examples:

Gemini Service
PDF Service
Embedding Service
Vector Service
Workflow Service

---

## Workflow-Based Automation

Complex features must be implemented as workflows.

Example:

Resume Analysis Workflow

Resume Upload
↓
Text Extraction
↓
Resume Analysis
↓
Skills Extraction
↓
Recommendation Generation
↓
Response

---

# System Components

## Frontend Layer

Technology:

* React.js
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui

Purpose:

Provide the user interface.

Responsibilities:

* User interaction
* Form handling
* File uploads
* Chat interface
* Dashboard display
* API communication

The frontend must never directly interact with databases or AI models.

All communication occurs through FastAPI.

---

# Frontend Architecture

src/

pages/
components/
hooks/
services/
types/
utils/

---

## Pages

Purpose:

Represent application screens.

Examples:

Home Page

Chat Page

Document Upload Page

Resume Analyzer Page

Interview Generator Page

Settings Page

---

## Components

Purpose:

Reusable UI elements.

Examples:

Navbar

Sidebar

Chat Window

Message Card

Upload Box

Analysis Card

Loading Spinner

---

## Services

Purpose:

Handle API communication.

Examples:

chatService.ts

documentService.ts

resumeService.ts

workflowService.ts

---

# Backend Layer

Technology:

* Python
* FastAPI

Purpose:

Expose APIs and coordinate business operations.

Responsibilities:

* Request validation
* Authentication
* Routing
* Service orchestration

---

# Backend Architecture

backend/

api/
services/
workflows/
models/
schemas/
database/
utils/

main.py

---

# API Layer

Purpose:

Receive requests from frontend.

Responsibilities:

* Validate requests
* Call services
* Return responses

Business logic must never be implemented here.

---

## API Modules

chat.py

upload.py

rag.py

resume.py

workflow.py

summary.py

---

# Service Layer

Purpose:

Contains reusable business logic.

Responsibilities:

* AI interactions
* File processing
* Embedding generation
* Database operations

---

## Services

Gemini Service

Purpose:

Handle communication with Gemini API.

Responsibilities:

* Prompt creation
* Response generation
* Error handling

---

PDF Service

Purpose:

Extract text from uploaded documents.

Responsibilities:

* Read PDFs
* Read DOCX files
* Text extraction

---

Embedding Service

Purpose:

Generate vector embeddings.

Responsibilities:

* Convert text into vectors
* Normalize embeddings

Model:

all-MiniLM-L6-v2

---

Vector Service

Purpose:

Manage FAISS vector database.

Responsibilities:

* Create vector index
* Store embeddings
* Similarity search

---

Workflow Service

Purpose:

Execute multi-step workflows.

Responsibilities:

* Coordinate services
* Manage execution sequence
* Generate workflow outputs

---

# Workflow Layer

Purpose:

Handle complete business processes.

Complex features should be implemented here.

---

## Resume Analysis Workflow

Input:

Resume File

Steps:

Extract Text
↓
Generate Summary
↓
Extract Skills
↓
Analyze Strengths
↓
Generate Recommendations

Output:

Resume Analysis Report

---

## Interview Generation Workflow

Input:

Resume File

Steps:

Analyze Resume
↓
Extract Skills
↓
Generate HR Questions
↓
Generate Technical Questions
↓
Generate Project Questions

Output:

Interview Preparation Report

---

## Document Summarization Workflow

Input:

Document

Steps:

Extract Content
↓
Identify Key Sections
↓
Generate Summary

Output:

Structured Summary

---

# AI Architecture

AI Provider:

Google Gemini

Model:

Gemini 2.5 Flash

Responsibilities:

* Chat
* Summarization
* Resume Analysis
* Interview Question Generation

AI must never directly access uploaded documents.

Document information must first pass through the retrieval layer.

---

# RAG Architecture

Purpose:

Provide document-aware AI responses.

---

## RAG Flow

Upload Document
↓
Extract Text
↓
Chunk Text
↓
Generate Embeddings
↓
Store in FAISS
↓
User Question
↓
Retrieve Relevant Chunks
↓
Build Context
↓
Send Context to Gemini
↓
Generate Response

---

# Document Processing Architecture

Supported Formats:

* PDF
* DOCX
* TXT

Flow:

Upload
↓
Validation
↓
Text Extraction
↓
Chunking
↓
Embedding Generation
↓
Vector Storage

---

# Database Architecture

Database:

PostgreSQL

Purpose:

Store structured application data.

Does not store embeddings.

Embeddings are stored in FAISS.

---

# Database Responsibilities

Store:

Users

Documents

Chat History

Analysis Results

Workflow History

System Logs

---

# Vector Database Architecture

Technology:

FAISS

Purpose:

Store embeddings for retrieval.

Responsibilities:

* Vector indexing
* Similarity search
* Context retrieval

---

# Security Architecture

Authentication Layer

↓

Authorization Layer

↓

API Layer

↓

Services

---

## Security Principles

Validate all requests.

Validate all uploads.

Protect AI endpoints.

Protect workflow endpoints.

Store secrets only in environment variables.

Never expose API keys.

---

# Deployment Architecture

Frontend

Vercel

↓

Backend

Render

↓

Gemini API

↓

PostgreSQL

↓

FAISS Storage

---

# Error Handling Architecture

Frontend

↓

API Validation

↓

Service Validation

↓

Exception Handling

↓

Standardized Error Response

---

## Standard Response Format

Success Response

{
"success": true,
"message": "Operation successful",
"data": {}
}

Error Response

{
"success": false,
"message": "Operation failed",
"errors": []
}

---

# Future Architecture Extensions

Phase 2

* Authentication
* User Profiles
* Document Collections

Phase 3

* Multi-Agent System
* Workflow Builder
* Team Collaboration

Phase 4

* Voice Assistant
* Real-Time Notifications
* AI Memory System

---

# Architecture Rules

1. Controllers must remain thin.
2. Business logic belongs in services.
3. Multi-step operations belong in workflows.
4. Embeddings belong in FAISS.
5. Structured data belongs in PostgreSQL.
6. Frontend never accesses AI directly.
7. Frontend never accesses databases directly.
8. AI interactions must be isolated.
9. RAG retrieval must occur before document-based AI responses.
10. Every new feature must follow this architecture.
