from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The generated response text")
    confidence: float = Field(..., description="Confidence score from 0-100")
