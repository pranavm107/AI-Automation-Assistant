from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse, description="Send a user message to Gemini and return a response.")
async def generate_chat_response(request: ChatRequest):
    """
    Handle incoming chat requests by passing the user message to the ChatService.
    
    Args:
        request (ChatRequest): The validated chat request containing the user message.
        
    Returns:
        ChatResponse: The structured response containing the AI's answer.
    """
    chat_service = ChatService()
    return chat_service.chat(request.message)
