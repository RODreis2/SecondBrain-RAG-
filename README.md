SecondBrain
===========

Local knowledge assistant powered by PDF books and a local LLM.

Overview
--------
SecondBrain is a lightweight Python prototype that loads PDF documents from a local books/ folder,
creates a vector store using embeddings, and answers user questions by querying a local LLM via LangChain.
The system is designed to be run entirely on your machine with no external API calls (except for model dependencies).

Key ideas:
- Read and index PDFs from your book collection.
- Turn text into semantic vectors with a transformer model.
- Use a local language model (Ollama) to answer questions based on the indexed context.
- Simple REPL (read-eval-print loop) chat interface for interactive Q&A.

Status
------
- Prototype ready for local experimentation.
- No secrets or credentials are committed in this repository. See .gitignore for ignored files.

Prerequisites
-------------
- Python 3.14 (as per pyproject.toml)
- Ollama installed and running with a model named llm "llama3" (as used in src/main.py)
- PDFs placed in books/ directory (glob ./books/*.pdf)
- A Python virtual environment (recommended):
  - python3.14 -m venv .venv
  - source .venv/bin/activate
- Dependencies can be installed from the pyproject.toml description. Typical core packages include:
  - langchain, langchain-ollama, langchain-huggingface, langchain-community, pypdf, pillow, etc.

Run locally
---------
1) Ensure Ollama is running and the llm model is available (llama3).
2) Place PDFs inside books/ (or other configured sources).
3) Prepare a Python environment and install dependencies, then run:
   python src/main.py
4) In the interactive prompt, type your questions. Type exit to quit.

How it works (high level)
------------------------
- Load PDFs from books/ and extract text.
- Split text into chunks with a RecursiveCharacterTextSplitter.
- Create embeddings with sentence-transformers/all-mpnet-base-v2 and build a FAISS vector store.
- The chat loop uses an Ollama LLM via LangChain to answer questions based on the retrieved context.
- The prompt template guides the LLM to answer using the provided context.

Directory layout (important files)
- src/
  - main.py: Main chat application, loads books, builds embeddings, and runs the REPL.
- books/
  - (PDF files should be placed here for indexing)
- pyproject.toml: Project metadata and dependency declarations.
- .gitignore: Secrets and build artifacts are ignored.

Customization
-----------
- To change the model, update the model parameter in src/main.py.
- To adjust chunking behavior, modify the chunk_size and chunk_overlap in the text splitter.
- To swap embeddings, modify the embeddings = HuggingFaceEmbeddings(...) line.

Security and privacy
---------------------
- No secrets are committed in this repository. A .gitignore guards common sensitive files.
- Data processing happens locally; ensure your PDFs do not contain restricted information if you share the workspace.

Known limitations
- Requires local LLM setup (Ollama) and a model named llama3; if not available, the chat will fail.
- The current REPL is basic and intended for experimentation.
- If books/ is empty or missing, there will be no contextual answers.

Contributing
- This is a small prototype. If you want to contribute, start by clarifying a local testing plan and ensuring your environment can run the app.

License
- Not specified in this repository. You can apply your preferred license if you plan to share this project.
