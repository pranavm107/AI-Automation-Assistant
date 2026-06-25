# Deployment Guide

## Prerequisites

* Docker
* Docker Compose
* Gemini API Key

---

## Environment Variables

Create:

backend/.env

Required Variables:

DATABASE_URL=
GEMINI_API_KEY=
UPLOAD_DIR=
VECTOR_STORE_DIR=

---

## Build Containers

docker compose build

---

## Start Application

docker compose up -d

---

## Run Database Migrations

docker compose exec backend alembic upgrade head

---

## Verify Backend

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Verify Frontend

[http://localhost:5173](http://localhost:5173)

---

## Production Recommendations

### Reverse Proxy

Use Nginx

### SSL

Use Let's Encrypt

### Database

Use Managed PostgreSQL

### File Storage

Use AWS S3

### Monitoring

* Prometheus
* Grafana
* Sentry

### Backups

Daily Database Backup

Weekly Vector Store Backup

---

## Deployment Checklist

* Environment Variables Configured
* Database Connected
* Alembic Applied
* Gemini API Verified
* Frontend Build Successful
* SSL Enabled
* Backups Configured

Deployment Status: READY
