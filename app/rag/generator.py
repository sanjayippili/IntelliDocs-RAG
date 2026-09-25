from app.rag.embeddings import llm


def generate_answer(question: str, documents):

    # Create context from retrieved documents
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer cannot be found in the context, say:

"I don't have enough information in the provided documents."

Do not use outside knowledge.
Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        # Call Gemini
        response = llm.invoke(prompt)

        content = response.content

        # Normal text response
        if isinstance(content, str):
            return content

        # Handle list response
        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):

                    text_parts.append(item)

            return "\n".join(text_parts)

        return str(content)

    except Exception as e:

        error_message = str(e)

        # Gemini quota / rate limit error
        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
            or "quota" in error_message.lower()
        ):

            return (
                "Gemini API quota has been exhausted.\n\n"
                "Please wait for the quota to reset "
                "or check your Gemini API quota and billing settings."
            )

        # Other Gemini/API errors
        return (
            "Sorry, I could not generate an answer right now.\n\n"
            "Please try again later."
        )