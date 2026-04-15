from app.rag.vectorstore import get_vectorstore

def get_retriever(k: int = 3):
    """
    Returns the vectorstore retriever configured to fetch the top `k` chunks.
    This component can be used in LCEL chains.
    """
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})
