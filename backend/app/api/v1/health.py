from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    return {
        "success": True,
        "message": "AI Automation Assistant API is running"
    }
