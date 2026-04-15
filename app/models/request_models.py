from pydantic import BaseModel, Field
from typing import Literal

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="The unique user identifier")
    message: str = Field(..., description="The user's medical query")
    role: Literal["patient", "student"] = Field(..., description="The target persona for the response")
