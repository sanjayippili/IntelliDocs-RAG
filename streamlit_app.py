import os
import streamlit as st

from app.loaders.document_loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import (
    add_documents,
    delete_document,
    delete_all_documents
)
from app.rag.retriever import retrieve_documents
from app.rag.generator import generate_answer
from app.utils.config import UPLOAD_DIR


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RAG Application",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# DEEP OCEAN THEME
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APPLICATION
       ===================================================== */

    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       TITLE
       ===================================================== */

    h1 {
        color: #0C4A6E !important;
        font-weight: 750 !important;
    }


    /* =====================================================
       CHAT HEADING
       ===================================================== */

    h2 {
        color: #075985 !important;
        font-weight: 700 !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #EFF6FF !important;
        border-right: 1px solid #BAE6FD !important;
    }


    /* =====================================================
       SIDEBAR HEADINGS
       ===================================================== */

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #075985 !important;
        font-weight: 700 !important;
    }


    /* =====================================================
       SIDEBAR TEXT
       ===================================================== */

    section[data-testid="stSidebar"] p {
        color: #334155 !important;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #0284C7 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }


    /* =====================================================
       ALL STREAMLIT BUTTONS
       ===================================================== */

    div.stButton > button,
    div.stButton > button[kind="secondary"],
    div.stButton > button[kind="primary"] {

        background-color: #0369A1 !important;

        color: #FFFFFF !important;

        border: 1px solid #0369A1 !important;

        border-radius: 8px !important;

        font-weight: 600 !important;

        box-shadow: none !important;
    }


    /* =====================================================
       BUTTON TEXT
       ===================================================== */

    div.stButton > button p {

        color: #FFFFFF !important;

        font-weight: 600 !important;
    }


    /* =====================================================
       BUTTON HOVER
       ===================================================== */

    div.stButton > button:hover {

        background-color: #0284C7 !important;

        color: #FFFFFF !important;

        border: 1px solid #0284C7 !important;

        box-shadow: none !important;
    }


    /* =====================================================
       BUTTON HOVER TEXT
       ===================================================== */

    div.stButton > button:hover p {

        color: #FFFFFF !important;
    }


    /* =====================================================
       BUTTON FOCUS
       ===================================================== */

    div.stButton > button:focus {

        background-color: #0369A1 !important;

        color: #FFFFFF !important;

        border: 1px solid #0369A1 !important;

        box-shadow: 0 0 0 2px rgba(3, 105, 161, 0.20) !important;
    }


    /* =====================================================
       BUTTON FOCUS TEXT
       ===================================================== */

    div.stButton > button:focus p {

        color: #FFFFFF !important;
    }


    /* =====================================================
       BUTTON ACTIVE
       ===================================================== */

    div.stButton > button:active {

        background-color: #075985 !important;

        color: #FFFFFF !important;

        border: 1px solid #075985 !important;
    }


    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    section[data-testid="stSidebar"] div.stButton > button {

        background-color: #0369A1 !important;

        color: #FFFFFF !important;

        border: 1px solid #0369A1 !important;

        border-radius: 8px !important;

        font-weight: 600 !important;

        box-shadow: none !important;
    }


    /* =====================================================
       SIDEBAR BUTTON TEXT
       ===================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button p {

        color: #FFFFFF !important;

        font-weight: 600 !important;
    }


    /* =====================================================
       SIDEBAR BUTTON HOVER
       ===================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button:hover {

        background-color: #0284C7 !important;

        color: #FFFFFF !important;

        border: 1px solid #0284C7 !important;
    }


    /* =====================================================
       SIDEBAR BUTTON HOVER TEXT
       ===================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button:hover p {

        color: #FFFFFF !important;
    }


    /* =====================================================
       SIDEBAR BUTTON FOCUS
       ===================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button:focus {

        background-color: #0369A1 !important;

        color: #FFFFFF !important;

        border: 1px solid #0369A1 !important;

        box-shadow: none !important;
    }


    /* =====================================================
       SIDEBAR BUTTON ACTIVE
       ===================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button:active {

        background-color: #075985 !important;

        color: #FFFFFF !important;

        border: 1px solid #075985 !important;
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }


    div[data-testid="stChatInput"] textarea {

        background-color: #FFFFFF !important;

        border: 2px solid #0EA5E9 !important;

        color: #0F172A !important;

        border-radius: 12px !important;
    }


    div[data-testid="stChatInput"] textarea:focus {

        border-color: #0284C7 !important;

        box-shadow: 0 0 8px rgba(14, 165, 233, 0.15) !important;
    }


    /* =====================================================
       CHAT MESSAGES
       ===================================================== */

    div[data-testid="stChatMessage"] {

        background-color: #FFFFFF !important;

        border: 1px solid #BAE6FD !important;

        border-radius: 12px !important;

        margin-bottom: 12px !important;

        padding: 10px !important;
    }


    /* =====================================================
       DOCUMENT CARDS
       ===================================================== */

    .document-item {

        background-color: #FFFFFF;

        border-left: 4px solid #0EA5E9;

        border-radius: 8px;

        padding: 10px;

        margin-bottom: 7px;

        color: #334155;

        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }


    /* =====================================================
       SOURCE CARDS
       ===================================================== */

    .source-item {

        background-color: #FFFFFF;

        border-left: 4px solid #0284C7;

        border-radius: 8px;

        padding: 10px;

        margin-bottom: 7px;

        color: #334155;

        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border-color: #BAE6FD !important;
    }


    /* =====================================================
       ALERT
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "documents" not in st.session_state:
    st.session_state.documents = []


if "sources" not in st.session_state:
    st.session_state.sources = []


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if "delete_all_confirmation" not in st.session_state:
    st.session_state.delete_all_confirmation = False


if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_file_path(file_name):

    return os.path.join(
        UPLOAD_DIR,
        file_name
    )


# ============================================================
# CLEAR CHAT
# ============================================================

def clear_chat():

    st.session_state.chat_history = []

    st.session_state.sources = []


# ============================================================
# CONFIRM DELETE ALL
# ============================================================

def confirm_delete_all():

    delete_all_documents()

    if os.path.exists(UPLOAD_DIR):

        for file_name in os.listdir(UPLOAD_DIR):

            file_path = os.path.join(
                UPLOAD_DIR,
                file_name
            )

            if os.path.isfile(file_path):

                os.remove(file_path)


    st.session_state.documents = []

    st.session_state.sources = []

    st.session_state.chat_history = []

    st.session_state.delete_all_confirmation = False

    st.session_state.uploader_key += 1


# ============================================================
# CANCEL DELETE ALL
# ============================================================

def cancel_delete_all():

    st.session_state.delete_all_confirmation = False


# ============================================================
# TITLE
# ============================================================

st.title(
    "📚 Upload Your Own Documents"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Upload Documents"
)


# ============================================================
# FILE UPLOADER
# ============================================================

uploaded_files = st.sidebar.file_uploader(
    "Choose documents",
    type=[
        "pdf",
        "docx",
        "txt",
        "csv",
        "json"
    ],
    accept_multiple_files=True,
    key=f"document_uploader_{st.session_state.uploader_key}"
)


# ============================================================
# SELECTED DOCUMENTS
# ============================================================

if uploaded_files:

    st.sidebar.subheader(
        "Selected Documents"
    )


    for uploaded_file in uploaded_files:

        st.sidebar.write(
            f"📄 {uploaded_file.name}"
        )


    # ========================================================
    # PROCESS DOCUMENTS
    # ========================================================

    if st.sidebar.button(
        "Process Documents"
    ):

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )


        for uploaded_file in uploaded_files:

            file_path = get_file_path(
                uploaded_file.name
            )


            # ------------------------------------------------
            # SAVE FILE
            # ------------------------------------------------

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )


            # ------------------------------------------------
            # LOAD DOCUMENT
            # ------------------------------------------------

            documents = load_document(
                file_path
            )


            # ------------------------------------------------
            # SPLIT DOCUMENT
            # ------------------------------------------------

            chunks = split_documents(
                documents
            )


            # ------------------------------------------------
            # ADD TO CHROMADB
            # ------------------------------------------------

            add_documents(
                chunks
            )


            # ------------------------------------------------
            # SAVE DOCUMENT NAME
            # ------------------------------------------------

            if uploaded_file.name not in st.session_state.documents:

                st.session_state.documents.append(
                    uploaded_file.name
                )


        st.success(
            "Documents processed successfully."
        )


# ============================================================
# CURRENT DOCUMENTS
# ============================================================

if st.session_state.documents:

    st.sidebar.divider()

    st.sidebar.subheader(
        "Current Documents"
    )


    for document_name in st.session_state.documents:

        st.sidebar.markdown(
            f"""
            <div class="document-item">
                📄 {document_name}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # DELETE DOCUMENT
        # ----------------------------------------------------

        if st.sidebar.button(
            "Delete",
            key=f"delete_{document_name}"
        ):

            file_path = get_file_path(
                document_name
            )


            # Delete ChromaDB vectors
            delete_document(
                file_path
            )


            # Delete original file
            if os.path.exists(file_path):

                os.remove(
                    file_path
                )


            # Remove document from session
            st.session_state.documents.remove(
                document_name
            )


            # Remove source
            st.session_state.sources = [
                source
                for source in st.session_state.sources
                if source != file_path
            ]


            st.rerun()


# ============================================================
# CHAT HEADER
# ============================================================

chat_col, clear_chat_col = st.columns(
    [6, 1]
)


with chat_col:

    st.header(
        "Chat"
    )


# ============================================================
# CLEAR CHAT BUTTON
# ============================================================

with clear_chat_col:

    st.write("")

    st.button(
        "Clear Chat",
        on_click=clear_chat,
        key="clear_chat_button"
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for chat in st.session_state.chat_history:

    with st.chat_message(
        "user"
    ):

        st.write(
            chat["question"]
        )


    with st.chat_message(
        "assistant"
    ):

        st.write(
            chat["answer"]
        )


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about your documents"
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    question = question.strip()


    if question:

        # ----------------------------------------------------
        # RETRIEVE
        # ----------------------------------------------------

        retrieved_documents = retrieve_documents(
            question
        )


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        question_sources = []


        for document in retrieved_documents:

            source = document.metadata.get(
                "source"
            )


            if source and source not in question_sources:

                question_sources.append(
                    source
                )


        st.session_state.sources = (
            question_sources
        )


        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        answer = generate_answer(
            question,
            retrieved_documents
        )


        # ----------------------------------------------------
        # CHAT HISTORY
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )


        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )


        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )


# ============================================================
# SOURCES
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "Sources"
)


if st.session_state.sources:

    for source in st.session_state.sources:

        st.sidebar.markdown(
            f"""
            <div class="source-item">
                📄 {os.path.basename(source)}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.sidebar.write(
        "No sources yet."
    )


# ============================================================
# DELETE ALL DOCUMENTS
# ============================================================

st.sidebar.divider()


if st.sidebar.button(
    "Delete All Documents",
    key="delete_all_button"
):

    st.session_state.delete_all_confirmation = True


# ============================================================
# DELETE ALL CONFIRMATION
# ============================================================

if st.session_state.delete_all_confirmation:

    st.sidebar.warning(
        "This will delete all uploaded documents "
        "and their ChromaDB data."
    )


    confirm_col, cancel_col = st.sidebar.columns(
        2
    )


    # --------------------------------------------------------
    # CONFIRM
    # --------------------------------------------------------

    with confirm_col:

        st.button(
            "Confirm",
            key="confirm_delete_all",
            on_click=confirm_delete_all
        )


    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    with cancel_col:

        st.button(
            "Cancel",
            key="cancel_delete_all",
            on_click=cancel_delete_all
        )