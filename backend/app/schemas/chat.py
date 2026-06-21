from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="The user's message")

class ChatResponseData(BaseModel):
    answer: str

class ChatResponse(BaseModel):
    success: bool
    message: str
    data: ChatResponseData
