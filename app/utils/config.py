import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# ChromaDB configuration
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "rag_documents"


# Upload directory
UPLOAD_DIR = "data/uploads"


# RAG configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5


# Validate API key
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to the .env file."
    )