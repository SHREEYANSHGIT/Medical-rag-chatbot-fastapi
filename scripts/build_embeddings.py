import os
import sys
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


# Ensure script picks up env variables from root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
sys.path.append(project_root)

from dotenv import load_dotenv
load_dotenv()

from app.rag.embeddings import get_embeddings

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./vectorstore")

def build_embeddings(pdf_path: str = "data/medical_book.pdf"):
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}.")
        print("Please place your medical_book.pdf in the 'data' directory.")
        return

    print(f"Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print(f"Loaded {len(docs)} pages. Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(docs)
    
    print(f"Created {len(chunks)} chunks. Building vectorstore...")
    embeddings = get_embeddings()
    
    # Initialize and persist Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )
    
    print(f"Success! Vector database stored at '{CHROMA_PERSIST_DIR}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, default="data/medical_book.pdf", help="Path to the Medical Book PDF")
    args = parser.parse_args()
    build_embeddings(args.pdf)
