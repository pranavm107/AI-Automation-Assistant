import logging
from app.services.gemini_service import GeminiService
from app.schemas.chat import ChatResponse, ChatResponseData

logger = logging.getLogger(__name__)

class ChatService:
    """
    Service responsible for orchestrating chat operations.
    Handles prompt construction and delegates AI generation to the GeminiService.
    """
    def __init__(self):
        self.gemini_service = GeminiService()
    
    def chat(self, message: str) -> ChatResponse:
        """
        Processes a user message and returns the AI response.
        
        Args:
            message (str): The user's input message.
            
        Returns:
            ChatResponse: The structured response object.
        """
        logger.info(f"Processing chat message of length: {len(message)}")
        
        system_prompt = (
            "You are AI Automation Assistant.\n\n"
            "Provide:\n"
            "* Clear answers\n"
            "* Professional responses\n"
            "* Concise explanations\n"
            "* Accurate information\n\n"
            "User Input:\n"
            f"{message}"
        )
        
        answer = self.gemini_service.generate_response(system_prompt)
        logger.info("Successfully generated chat response.")
        
        return ChatResponse(
            success=True,
            message="Chat response generated successfully",
            data=ChatResponseData(answer=answer)
        )
