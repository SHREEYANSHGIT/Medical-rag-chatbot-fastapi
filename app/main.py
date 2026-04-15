from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_chat import router as chat_router

app = FastAPI(title="Medical RAG AI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Medical RAG AI is running"}

