import os
from langchain_chroma import Chroma
from app.rag.embeddings import get_embeddings
from dotenv import load_dotenv

load_dotenv()


CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./vectorstore")

_vectorstore_instance = None

def get_vectorstore() -> Chroma:
    """
    Initializes and returns the Chroma vectorstore (Singleton).
    """
    global _vectorstore_instance
    if _vectorstore_instance is None:
        embeddings = get_embeddings()
        _vectorstore_instance = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings
        )
    return _vectorstore_instance
