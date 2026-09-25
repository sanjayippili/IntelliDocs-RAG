# LangChain RAG Production Application

A production-style Retrieval-Augmented Generation (RAG) application built using LangChain, Gemini, ChromaDB, and Streamlit.

This application allows users to dynamically upload their own documents and ask questions about the uploaded content. The system loads the documents, splits them into smaller chunks, converts the chunks into vector embeddings using Gemini, stores the embeddings in ChromaDB, retrieves relevant chunks based on the user's question, and uses a Gemini language model to generate an answer from the retrieved context.

## Project Overview

The application follows this RAG pipeline:

User Uploads Documents
↓
Document Loading
↓
Document Chunking
↓
Gemini Embeddings
↓
ChromaDB
↓
Similarity Search
↓
Relevant Document Chunks
↓
Gemini LLM
↓
Generated Answer

The application supports dynamic document uploading, document deletion, source tracking, chat history, and question answering through a Streamlit interface.

## Features

* Dynamic document uploading
* Multiple document upload
* PDF support
* DOCX support
* TXT support
* CSV support
* JSON support
* Document chunking
* Gemini embeddings
* ChromaDB vector database
* Similarity-based document retrieval
* Gemini LLM for answer generation
* Context-based question answering
* Source filename display
* Individual document deletion
* Delete all documents
* Delete all confirmation
* Chat history
* Clear chat functionality
* Dynamic ChromaDB creation
* Gemini API error handling
* Streamlit user interface

## Technologies Used

Python - Programming language

LangChain - RAG framework

Gemini - Embeddings and Large Language Model

ChromaDB - Vector database

Streamlit - Web application interface

PyPDF - PDF document loading

Docx2txt - DOCX document loading

Pandas - CSV/data processing

Python-dotenv - Environment variable management

## Supported File Formats

The application currently supports:

PDF
DOCX
TXT
CSV
JSON

Users can upload multiple documents through the Streamlit interface.

## Project Structure

LangChain-RAG-Production/

├── app/

│   ├── loaders/

│   │   ├── pdf_loader.py

│   │   ├── docx_loader.py

│   │   ├── txt_loader.py

│   │   ├── csv_loader.py

│   │   ├── json_loader.py

│   │   └── document_loader.py

│   │

│   ├── rag/

│   │   ├── splitter.py

│   │   ├── embeddings.py

│   │   ├── vectorstore.py

│   │   ├── retriever.py

│   │   └── generator.py

│   │

│   └── utils/

│       └── config.py

│

├── data/

│   └── uploads/

│

├── chroma_db/

├── streamlit_app.py

├── requirements.txt

├── .env

├── .env.example

├── .gitignore

└── README.md

The `chroma_db/` and `data/uploads/` directories are used locally and should not be committed to GitHub.

## RAG Pipeline

### 1. Document Upload

The user uploads one or more documents through the Streamlit interface.

For example:

document.pdf
company_policy.docx
notes.txt
employees.csv
data.json

Uploaded files are stored locally in:

data/uploads/

### 2. Document Loading

The application identifies the uploaded file extension and selects the appropriate document loader.

PDF → PyPDFLoader

DOCX → Docx2txtLoader

TXT → TextLoader

CSV → CSVLoader

JSON → Custom JSON Loader

The common document loader handles the file type detection and calls the appropriate loader.

### 3. Document Chunking

Large documents are divided into smaller chunks before generating embeddings.

Current configuration:

Chunk Size = 500

Chunk Overlap = 50

The project uses `RecursiveCharacterTextSplitter`.

Chunk overlap helps preserve some context between neighboring chunks.

### 4. Gemini Embeddings

Each document chunk is converted into a numerical vector using the Gemini embedding model.

Embedding model:

gemini-embedding-001

The generated vectors represent the semantic meaning of the document chunks.

### 5. ChromaDB

The generated embeddings are stored in ChromaDB.

ChromaDB is used as the vector database for the application.

Document Chunk
↓
Gemini Embedding
↓
Vector
↓
ChromaDB

ChromaDB is created and updated locally when documents are processed.

### 6. User Question

The user asks a question through the Streamlit chat interface.

For example:

What is the case number?

### 7. Similarity Retrieval

The question is sent to ChromaDB.

ChromaDB performs a similarity search and retrieves the document chunks that are most relevant to the question.

Current configuration:

TOP_K = 5

### 8. Context Generation

The retrieved document chunks are combined and passed as context to the Gemini language model.

Retrieved Chunk 1
Retrieved Chunk 2
Retrieved Chunk 3
...

### 9. Gemini Answer Generation

The retrieved context and user question are sent to the Gemini language model.

The prompt instructs the model to:

* Use only the provided context
* Not use outside knowledge
* Not make up information
* Return a fallback response when the answer is not available in the documents

Fallback response:

"I don't have enough information in the provided documents."

## Application Interface

The application contains two main areas.

### Sidebar

The sidebar contains:

Upload Documents

Selected Documents

Process Documents

Current Documents

Sources

Delete All Documents

The sidebar displays the filenames of the documents used to answer the current question.

### Chat Area

The main area contains:

Chat

Question

Answer

Users can ask multiple questions about their uploaded documents.

The chat history is maintained during the session.

## Document Management

### Individual Document Delete

Users can delete an individual uploaded document.

The application removes the original document and its corresponding ChromaDB vectors.

Other uploaded documents remain available.

### Delete All Documents

The application provides a Delete All Documents option with confirmation.

After confirmation, the application removes all uploaded documents, their corresponding ChromaDB vectors, current sources, and chat history.

## Source Tracking

After a question is asked, the application identifies the source filenames from the retrieved document chunks.

For example:

Sources

company_policy.pdf

employee_handbook.docx

Only the source documents used for the current question are displayed.

Retrieved chunks themselves are not displayed in the UI.

## Configuration

The project uses an environment variable for the Gemini API key.

Create a `.env` file in the project root.

Add:

GOOGLE_API_KEY=your_gemini_api_key

The actual API key must never be committed to GitHub.

## .env.example

For GitHub, create a `.env.example` file containing:

GOOGLE_API_KEY=your_gemini_api_key_here

The `.env.example` file is only a template.

Users should create their own `.env` file and add their own Gemini API key.

## Installation

### 1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Move into the project directory:

cd LangChain-RAG-Production

### 2. Create Virtual Environment

On Windows:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Gemini API Key

Create a `.env` file in the project root.

Add:

GOOGLE_API_KEY=your_gemini_api_key

## Run the Application

Start the Streamlit application:

streamlit run streamlit_app.py

The application will open in the browser.

## How to Use

### Step 1

Open the application.

### Step 2

Upload one or more supported documents.

Supported formats:

PDF
DOCX
TXT
CSV
JSON

### Step 3

Click:

Process Documents

The application will:

Load
↓
Split
↓
Embed
↓
Store in ChromaDB

### Step 4

Ask a question in the chat box.

For example:

What is the case number?

### Step 5

The application retrieves relevant document chunks and generates an answer using Gemini.

### Step 6

The source documents used for the answer are displayed in the sidebar.

## Error Handling

The application handles Gemini API resource and quota errors.

For example:

429 RESOURCE_EXHAUSTED

This error can occur when the Gemini API resource or quota limit is temporarily reached.

The application handles this condition and displays a user-friendly message instead of exposing a Python traceback.

Depending on the Gemini API usage limits, users may need to wait and try again.

## Security

The Gemini API key must not be stored directly in Python source code.

The following files and directories should not be committed to GitHub:

.env

chroma_db/

data/uploads/

The recommended `.gitignore` entries are:

.env

venv/

.venv/

**pycache**/

*.pyc

chroma_db/

data/uploads/

.ipynb_checkpoints/

.streamlit/secrets.toml

## Architecture

User
↓
Streamlit UI
↓
Document Upload
↓
Document Loaders
↓
Document Splitter
↓
Gemini Embeddings
↓
ChromaDB
↓
Similarity Search
↓
Relevant Chunks
↓
Gemini LLM
↓
Answer

## Key Configuration

Embedding Model:

gemini-embedding-001

LLM:

gemini-3.6-flash

Chunk Size:

500

Chunk Overlap:

50

Top K:

5

Vector Database:

ChromaDB

Framework:

LangChain

Frontend:

Streamlit

## Project Goals

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Document processing
* Document chunking
* Text embeddings
* Vector databases
* Semantic similarity search
* Context-based question answering
* LangChain integration
* Gemini integration
* Dynamic document management
* Streamlit application development

## Future Improvements

Possible future improvements include:

* Retrieval quality evaluation
* RAG evaluation metrics
* Hybrid search
* Reranking
* Conversation-aware retrieval
* Authentication
* User-specific document collections
* Document metadata filtering
* Cloud deployment
* Production monitoring
* Improved document processing
* Streaming Gemini responses

## Author

Sanjay Kumar Ippili

B.Tech - Information Technology

Interests:

Machine Learning
Python
Generative AI
RAG
LangChain
AI Agents
Data Science

## License

This project is intended for educational, portfolio, and demonstration purposes.
