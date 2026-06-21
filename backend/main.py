from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import health, chat
from app.core.exceptions import add_exception_handlers

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

add_exception_handlers(app)

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)

# TODO: Include other routers as they are implemented
# from app.api.v1 import documents, rag, resume, interview, summary, workflows
# app.include_router(chat.router, prefix=settings.API_V1_STR)
# app.include_router(documents.router, prefix=settings.API_V1_STR)
# app.include_router(rag.router, prefix=settings.API_V1_STR)
# app.include_router(resume.router, prefix=settings.API_V1_STR)
# app.include_router(interview.router, prefix=settings.API_V1_STR)
# app.include_router(summary.router, prefix=settings.API_V1_STR)
# app.include_router(workflows.router, prefix=settings.API_V1_STR)
