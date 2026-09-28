# LangChain RAG Document Assistant

A Streamlit application for asking questions about uploaded documents. It loads documents, splits their content into chunks, embeds those chunks with Google Gemini, stores them in a local ChromaDB collection, retrieves relevant chunks for each question, and asks Gemini to answer using the retrieved context.

This repository is a practical RAG demonstration. It is not a hardened multi-user production service: it has no authentication, authorization, tenant isolation, or deployment-specific secret management.

## Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Supported Documents](#supported-documents)
- [Project Layout](#project-layout)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run the Application](#run-the-application)
- [Using the Application](#using-the-application)
- [Configuration Defaults](#configuration-defaults)
- [Data, Persistence, and Privacy](#data-persistence-and-privacy)
- [Troubleshooting](#troubleshooting)
- [Current Limitations](#current-limitations)

## Features

- Upload one or more PDF, DOCX, TXT, CSV, and JSON files.
- Split loaded content into overlapping text chunks.
- Generate embeddings with Google's `gemini-embedding-001` model.
- Store and search vectors in a persistent local ChromaDB collection.
- Retrieve the five most similar chunks for a question.
- Generate context-based answers with Google's `gemini-3.6-flash` model.
- Display source filenames for the retrieved content.
- Delete an individual document or confirm deletion of all documents.
- Clear the current chat history.

## How It Works

```text
Upload files
    -> Load file contents
    -> Split into chunks (500 characters, 50-character overlap)
    -> Embed chunks with Gemini
    -> Store chunks and vectors in ChromaDB

Ask a question
    -> Embed/search the question through ChromaDB
    -> Retrieve up to five similar chunks
    -> Send question and retrieved context to Gemini
    -> Display the answer and source filenames
```

The answer prompt asks Gemini to use only the retrieved context and not invent information. If the answer is not found, the requested fallback is: `I don't have enough information in the provided documents.` This instruction helps guide the model but does not guarantee that every generated answer will be correct; check important answers against the source documents.

## Technology Stack

- Python
- Streamlit
- LangChain and LangChain integrations
- Google Gemini embeddings and chat model
- ChromaDB with a local persistent directory
- PyPDF, docx2txt, and pandas-backed CSV loading
- python-dotenv for loading `.env` configuration

Dependencies are listed in [`requirements.txt`](requirements.txt). They are not version-pinned, so installed versions may change over time.

## Supported Documents

| Extension | Loader | Notes |
| --- | --- | --- |
| `.pdf` | `PyPDFLoader` | Extracts PDF page text. Scanned pages may require OCR, which is not configured here. |
| `.docx` | `Docx2txtLoader` | Supports Word `.docx` files. |
| `.txt` | `TextLoader` | Reads as UTF-8. |
| `.csv` | `CSVLoader` | Loads CSV rows as documents. |
| `.json` | Project JSON loader | A JSON list is represented as one document per item; other JSON values become one document. |

The Streamlit file picker currently restricts uploads to these extensions. Legacy `.doc` files, spreadsheets, images, and OCR are not supported.

## Project Layout

```text
.
|-- app/
|   |-- loaders/
|   |   |-- csv_loader.py
|   |   |-- document_loader.py
|   |   |-- docx_loader.py
|   |   |-- json_loader.py
|   |   |-- pdf_loader.py
|   |   `-- txt_loader.py
|   |-- rag/
|   |   |-- embeddings.py
|   |   |-- generator.py
|   |   |-- retriever.py
|   |   |-- splitter.py
|   |   `-- vectorstore.py
|   `-- utils/
|       `-- config.py
|-- data/
|   `-- uploads/       # Uploaded originals (created when needed)
|-- chroma_db/         # Persistent local vector database
|-- streamlit_app.py   # Streamlit interface and application flow
|-- requirements.txt
`-- README.md
```

## Requirements

- Python 3.10 or newer is recommended.
- A Google Gemini API key with access to the configured embedding and chat models.
- Internet access when calling Gemini APIs.

## Installation

Run commands from the repository root.

1. Clone the repository and change into its directory:

   ```powershell
   git clone <repository-url>
   cd LangChain-RAG-Production
   ```

   Replace `<repository-url>` with the URL of your Git repository.

2. Create and activate a virtual environment. In Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install project dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the repository root and add your Gemini API key as described below.

## Configuration

The application reads `GOOGLE_API_KEY` from the environment. The included configuration calls `load_dotenv()`, which loads values from a root-level `.env` file.

Create `.env` in the project root:

```dotenv
GOOGLE_API_KEY=your_gemini_api_key
```

Use your own key; do not commit it or paste it into source code. The repository's `.gitignore` excludes `.env`, `chroma_db/`, and `data/uploads/`. If you publish or share the repository, keep those protections in place. For hosted deployment, configure the key using the hosting provider's secret-management mechanism rather than committing a secret file.

The app raises an error during configuration if `GOOGLE_API_KEY` is missing.

## Run the Application

With the virtual environment activated and `.env` configured, run:

```bash
streamlit run streamlit_app.py
```

Streamlit prints a local URL in the terminal and usually opens it in your browser. Stop the server with `Ctrl+C` in the terminal.

## Using the Application

1. Use the sidebar file picker to select one or more supported files.
2. Select **Process Documents**. The app saves each original under `data/uploads/`, loads and chunks its content, and adds the chunks to ChromaDB. Wait for the success message before asking questions.
3. Enter a question in the chat box. The app searches the stored chunks, sends the question and retrieved content to Gemini, then displays the answer and source filenames in the sidebar.
4. Ask more questions during the session. Use **Clear Chat** to clear the displayed conversation and current source list; it does not delete indexed documents.
5. Use an individual **Delete** button to remove that file and its matching vectors. **Delete All Documents** asks for confirmation before clearing uploaded files, vector records, the session document list, sources, and chat.

Example questions:

- `What are the main requirements in this policy?`
- `Which dates are mentioned in the report?`
- `Summarize the CSV records about the selected topic.`

Ask focused questions and verify consequential answers in the original documents.

## Configuration Defaults

The defaults are defined in [`app/utils/config.py`](app/utils/config.py) and [`app/rag/embeddings.py`](app/rag/embeddings.py):

| Setting | Default |
| --- | --- |
| Embedding model | `gemini-embedding-001` |
| Chat model | `gemini-3.6-flash` |
| Chunk size | `500` characters |
| Chunk overlap | `50` characters |
| Retrieved chunks (`TOP_K`) | `5` |
| ChromaDB directory | `chroma_db/` |
| ChromaDB collection | `rag_documents` |
| Upload directory | `data/uploads/` |

Changing chunking or model settings affects how documents are indexed and queried. If you change embedding models, re-index existing content so stored vectors are compatible with the active embedding model.

## Data, Persistence, and Privacy

- Uploaded originals are written to `data/uploads/`; vectors and document metadata are stored under `chroma_db/`.
- The ChromaDB directory is persistent across app restarts. The UI's current document-name list, source list, and chat history use Streamlit session state and are not a durable user/account history.
- This app uses one local collection and local directories. Anyone with access to the running app and its files may be able to interact with or inspect that data; there is no authentication or per-user separation.
- Uploaded document content and questions are sent to Gemini for embedding or answer generation. Do not upload sensitive material unless its handling is acceptable under your policies and the provider's terms.
- Uploaded files are saved using their original filenames. Files with the same name can overwrite one another, so use distinct filenames.
- Processing the same document repeatedly can add duplicate chunks to the vector collection. The current app does not deduplicate or update a previously indexed file automatically.
- Deleting a document removes vectors matching its stored source path and deletes the corresponding local upload. Deleting all also clears the ChromaDB records in the app's collection.

The `chroma_db/` and `data/uploads/` directories are ignored by Git and should generally remain local. Back them up separately if you need to preserve indexed data or originals.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `GOOGLE_API_KEY not found` | Confirm `.env` is in the repository root, the variable is spelled exactly `GOOGLE_API_KEY`, and the app is started from the project directory. |
| Gemini quota, rate limit, or `429` message | Check your Google AI quota and billing/project settings, then retry after the applicable limit resets. |
| Other Gemini request failures | Check network access, key validity, model availability for your account, and the terminal output for details. |
| A file fails to load | Confirm it is a valid supported format. TXT files are read as UTF-8; scanned PDFs may not contain extractable text. |
| Answers do not include expected information | Verify the text was extracted correctly, reprocess the document, and try a more specific question. Retrieval only supplies up to five matching chunks. |
| Document list is empty after restarting | The list is session state, even though local files and ChromaDB data persist. The current UI does not rebuild the list from the database on startup. |
| Import or dependency errors | Activate the intended virtual environment and reinstall dependencies with `pip install -r requirements.txt`. |

Gemini quota and other API errors during answer generation are converted into user-facing messages by the application. Document loading and embedding errors may still surface during processing.

## Current Limitations

- No authentication, user accounts, tenant isolation, or access controls.
- Local filesystem and local ChromaDB only; deployment and shared-storage behavior are not configured.
- No automatic OCR, hybrid search, reranking, retrieval evaluation, or streaming responses.
- No automatic vector deduplication, document update workflow, or startup reconstruction of the UI's document list.
- Conversation history is not used to reformulate retrieval queries; each question is searched independently.
- Dependencies are not pinned to exact versions, and this repository does not include a test suite or deployment configuration.

These boundaries matter before exposing the app to untrusted users or using it for sensitive or business-critical workloads.