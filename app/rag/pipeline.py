import os
from typing import AsyncGenerator, Tuple
from langchain_groq import ChatGroq
from app.rag.prompts import PATIENT_PROMPT, STUDENT_PROMPT
from app.rag.vectorstore import get_vectorstore
from app.rag.safety import detect_emergency, EMERGENCY_RESPONSE
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
TOP_K = int(os.getenv("TOP_K", "3"))

def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=TEMPERATURE,
        streaming=True
    )

def calculate_confidence(scores: list[float]) -> float:
    """
    Normalize similarity distance/score to a 0-100 percentage.
    Chroma typically returns L2 distance. Smaller distance = higher similarity.
    This is a simplistic mapping for MVP purposes.
    """
    if not scores:
        return 0.0
    
    avg_distance = sum(scores) / len(scores)
    
    # Simple heuristic to map distance to a confidence percentage
    # (Assuming smaller is better, with distance generally < 1.0 for good matches depending on model)
    confidence = max(0.0, 100.0 - (avg_distance * 50))
    return round(min(confidence, 100.0), 2)

async def generate_chat_response(message: str, role: str) -> Tuple[AsyncGenerator[str, None], float]:
    """
    Core RAG pipeline returning the text stream generator and confidence score.
    """
    if detect_emergency(message):
        # Emergency safety override
        async def emergency_stream():
            yield EMERGENCY_RESPONSE
        return emergency_stream(), 100.0

    vectorstore = get_vectorstore()
    
    # Retrieve documents and relevance scores
    docs_and_scores = vectorstore.similarity_search_with_score(message, k=TOP_K)
    
    context_text = "\n\n".join([doc.page_content for doc, _score in docs_and_scores])
    scores = [score for _doc, score in docs_and_scores]
    
    confidence = calculate_confidence(scores)
    
    # Determine appropriate prompt based on user role
    prompt_template = PATIENT_PROMPT if role == "patient" else STUDENT_PROMPT
    prompt_value = prompt_template.format(context=context_text, question=message)
    
    llm = get_llm()
    
    # Async generator to stream Groq LLM tokens
    async def response_stream() -> AsyncGenerator[str, None]:
        async for chunk in llm.astream(prompt_value):
            if chunk.content:
                yield chunk.content

    return response_stream(), confidence
