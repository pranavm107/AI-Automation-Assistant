# Production Release Checklist

## 1. Environment & Infrastructure
- [ ] Production `.env` file generated with secure `DATABASE_URL` and `GEMINI_API_KEY`.
- [ ] Database (PostgreSQL) hosted on a managed instance with daily automated backups.
- [ ] FAISS vector storage directory mounted to a persistent volume.
- [ ] Upload directory for documents mounted to a persistent volume (or swapped to S3).

## 2. Security
- [ ] FastAPI Swagger documentation disabled or secured in production.
- [ ] CORS configured to strictly allow only the production frontend URL.
- [ ] All API keys rotated before final deployment.

## 3. Deployment
- [ ] Frontend successfully built using `npm run build`.
- [ ] Frontend static assets deployed to CDN or served securely via Nginx.
- [ ] Backend containerized and deployed.
- [ ] Alembic migrations run successfully against the production database (`alembic upgrade head`).

## 4. Monitoring & Logging
- [ ] Application logs are being collected and shipped to a centralized dashboard.
- [ ] Basic uptime monitoring implemented for `/api/v1/health` endpoints.

## 5. Verification
- [ ] Successfully upload a test PDF in the production environment.
- [ ] Ensure RAG chat returns accurate results.
- [ ] Verify Job Matching algorithms complete without LLM timeouts.
- [ ] Verify Frontend routes directly (checking React Router fallback rules).

Go-Live Status: PENDING
