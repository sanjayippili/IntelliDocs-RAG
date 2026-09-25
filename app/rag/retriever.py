from app.rag.vectorstore import get_vectorstore
from app.utils.config import TOP_K


def retrieve_documents(question: str):

    vectorstore = get_vectorstore()

    documents = vectorstore.similarity_search(
        question,
        k=TOP_K
    )

    return documents