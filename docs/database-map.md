# AI Automation Assistant - Database Map

## Database Overview

Database Technology:

PostgreSQL

Purpose:

The database stores all structured application data.

The database does NOT store embeddings.

Embeddings are stored in FAISS.

PostgreSQL stores:

* Users
* Documents
* Chat History
* Analysis Results
* Workflow Executions
* Application Metadata

---

# Database Architecture

Frontend
↓
FastAPI
↓
Services
↓
PostgreSQL

Vector Data
↓
FAISS

AI Responses
↓
Gemini

---

# Design Principles

## Primary Keys

All tables use:

UUID

Example:

id UUID PRIMARY KEY

---

## Audit Columns

Every table should include:

created_at
updated_at

Purpose:

* Auditing
* Tracking
* Analytics

---

## Naming Convention

Tables:

snake_case

Examples:

users
documents
chat_history

Columns:

snake_case

Examples:

file_name
user_id
created_at

---

# Entity Relationship Diagram

User
│
├── Documents
│
├── Chat History
│
└── Workflow Executions

Document
│
├── Analysis Results
│
└── RAG Queries

---

# Table: users

Purpose:

Store user accounts.

Columns:

id UUID PRIMARY KEY

name VARCHAR(255)

email VARCHAR(255) UNIQUE

password_hash VARCHAR(255)

is_active BOOLEAN

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Relationships

users
↓
documents

users
↓
chat_history

users
↓
workflow_executions

---

# Table: documents

Purpose:

Store uploaded document metadata.

Columns:

id UUID PRIMARY KEY

user_id UUID

file_name VARCHAR(255)

original_name VARCHAR(255)

file_type VARCHAR(50)

file_size BIGINT

file_path TEXT

upload_status VARCHAR(50)

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Relationships

documents.user_id
→ users.id

documents
↓
analysis_results

documents
↓
rag_queries

---

# Table: chat_history

Purpose:

Store AI conversations.

Columns:

id UUID PRIMARY KEY

user_id UUID

question TEXT

answer TEXT

model_name VARCHAR(100)

response_time_ms INTEGER

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Relationships

chat_history.user_id
→ users.id

---

# Table: analysis_results

Purpose:

Store generated AI analysis.

Columns:

id UUID PRIMARY KEY

document_id UUID

analysis_type VARCHAR(100)

result JSONB

generated_by VARCHAR(100)

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Analysis Types

resume_analysis

document_summary

interview_questions

ats_analysis

custom_analysis

---

## Relationships

analysis_results.document_id
→ documents.id

---

# Table: rag_queries

Purpose:

Track document question answering.

Columns:

id UUID PRIMARY KEY

document_id UUID

question TEXT

answer TEXT

retrieved_chunks INTEGER

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Relationships

rag_queries.document_id
→ documents.id

---

# Table: workflow_executions

Purpose:

Track workflow execution history.

Columns:

id UUID PRIMARY KEY

user_id UUID

workflow_name VARCHAR(255)

status VARCHAR(50)

execution_time_ms INTEGER

result JSONB

started_at TIMESTAMP

completed_at TIMESTAMP

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Workflow Names

resume_analysis

interview_generation

document_summary

document_qa

custom_workflow

---

## Status Values

pending

running

completed

failed

cancelled

---

# Table: system_logs

Purpose:

Store application logs.

Columns:

id UUID PRIMARY KEY

log_level VARCHAR(50)

source VARCHAR(100)

message TEXT

metadata JSONB

created_at TIMESTAMP

updated_at TIMESTAMP

---

## Log Levels

INFO

WARNING

ERROR

DEBUG

CRITICAL

---

# Table: user_sessions (Future)

Purpose:

Store authentication sessions.

Columns:

id UUID PRIMARY KEY

user_id UUID

access_token TEXT

refresh_token TEXT

expires_at TIMESTAMP

created_at TIMESTAMP

updated_at TIMESTAMP

---

# Database Index Strategy

## Users

INDEX(email)

Purpose:

Fast login lookup.

---

## Documents

INDEX(user_id)

INDEX(file_type)

Purpose:

Fast document retrieval.

---

## Chat History

INDEX(user_id)

INDEX(created_at)

Purpose:

Conversation history retrieval.

---

## Analysis Results

INDEX(document_id)

INDEX(analysis_type)

Purpose:

Analysis filtering.

---

## Workflow Executions

INDEX(user_id)

INDEX(workflow_name)

INDEX(status)

Purpose:

Workflow monitoring.

---

# Constraints

## User Email

Must be unique.

UNIQUE(email)

---

## Foreign Keys

documents.user_id
→ users.id

analysis_results.document_id
→ documents.id

rag_queries.document_id
→ documents.id

workflow_executions.user_id
→ users.id

---

# JSON Storage Strategy

Use JSONB for:

analysis_results.result

workflow_executions.result

system_logs.metadata

Reason:

Flexible AI-generated output structures.

---

# Data Retention Strategy

Chat History

Retention:
12 months

---

System Logs

Retention:
6 months

---

Workflow Logs

Retention:
12 months

---

Analysis Results

Retention:
Permanent

---

# Soft Delete Strategy (Future)

Add:

deleted_at TIMESTAMP

Purpose:

Allow recovery of deleted records.

Applies To:

users

documents

analysis_results

---

# Database Security Rules

1. Never store API keys.
2. Never store plaintext passwords.
3. Always hash passwords.
4. Use foreign key constraints.
5. Validate all user input.
6. Protect sensitive data.
7. Log security-related events.
8. Use parameterized queries.

---

# Database Growth Considerations

Phase 1

Expected Users:
100

Expected Documents:
10,000

---

Phase 2

Expected Users:
10,000+

Expected Documents:
1,000,000+

---

Scalability Strategy

* Connection pooling
* Query optimization
* Index management
* Archiving old logs
* Read replicas (future)

---

# Database Rules

1. PostgreSQL stores structured data.
2. FAISS stores embeddings.
3. AI responses are stored in analysis_results.
4. Chat conversations are stored in chat_history.
5. Every table must contain audit columns.
6. Foreign keys must be enforced.
7. UUIDs must be used as primary keys.
8. Schema changes require documentation updates.

---

# Future Tables

user_preferences

saved_prompts

workflow_templates

agent_configurations

notification_settings

analytics_events

team_members

organization_accounts

These tables are reserved for future versions and should not be implemented until required.
