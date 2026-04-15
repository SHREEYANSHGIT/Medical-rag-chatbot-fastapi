import os
import time
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

load_dotenv()

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

class RobustHuggingFaceEmbeddings(HuggingFaceEndpointEmbeddings):
    """
    A wrapper around HuggingFaceEndpointEmbeddings that handles common API issues
    like model loading delays (which cause KeyError: 0 in LangChain).
    """
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        for i in range(3):
            try:
                return super().embed_documents(texts)
            except Exception as e:
                if "KeyError: 0" in str(e) or "loading" in str(e).lower():
                    time.sleep(5)
                    continue
                raise e
        return super().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        for i in range(3):
            try:
                return super().embed_query(text)
            except Exception as e:
                if "KeyError: 0" in str(e) or "loading" in str(e).lower():
                    time.sleep(5)
                    continue
                raise e
        return super().embed_query(text)

_embeddings_instance = None

def get_embeddings() -> RobustHuggingFaceEmbeddings:
    """
    Returns the Robust HuggingFace Endpoint embeddings model (Singleton).
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        if not HF_TOKEN:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in environment variables")
            
        _embeddings_instance = RobustHuggingFaceEmbeddings(
            huggingfacehub_api_token=HF_TOKEN,
            model=EMBEDDING_MODEL_NAME
        )
    return _embeddings_instance
