import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.request_models import ChatRequest
from app.rag.pipeline import generate_chat_response

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Handles streaming chat queries.
    Returns Server-Sent Events (SSE) with metadata first, then content chunks.
    """
    stream_generator, confidence = await generate_chat_response(request.message, request.role)
    
    async def sse_generator():
        # 1. Send confidence score and metadata
        meta_payload = json.dumps({"type": "metadata", "confidence": confidence})
        yield f"data: {meta_payload}\n\n"
        # 2. Generate full response by tracking the stream
        full_content = ""
        async for chunk in stream_generator:
            full_content += chunk
            
        # 3. Yield a single response containing the complete text
        content_payload = json.dumps({"type": "content", "content": full_content})
        yield f"data: {content_payload}\n\n"
                
        # 4. Final completion event
        done_payload = json.dumps({"type": "done"})
        yield f"data: {done_payload}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
