from langchain_chroma import Chroma

from app.rag.embeddings import embedding_model
from app.utils.config import CHROMA_DB_PATH, COLLECTION_NAME


# ==================================================
# GET VECTOR STORE
# ==================================================

def get_vectorstore():

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=CHROMA_DB_PATH
    )

    return vectorstore


# ==================================================
# ADD DOCUMENTS
# ==================================================

def add_documents(chunks):

    vectorstore = get_vectorstore()

    vectorstore.add_documents(
        chunks
    )

    return vectorstore


# ==================================================
# DELETE ONE DOCUMENT
# ==================================================

def delete_document(source: str):

    vectorstore = get_vectorstore()

    vectorstore._collection.delete(
        where={
            "source": {
                "$eq": source
            }
        }
    )


# ==================================================
# DELETE ALL DOCUMENTS
# ==================================================

def delete_all_documents():

    vectorstore = get_vectorstore()

    # Get all document IDs
    result = vectorstore._collection.get(
        include=[]
    )

    ids = result.get(
        "ids",
        []
    )

    # Delete all documents only if IDs exist
    if ids:

        vectorstore._collection.delete(
            ids=ids
        )