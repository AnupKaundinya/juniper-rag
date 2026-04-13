# Juniper Switch RAG Chatbot

🔗 **Live Demo**: [juniper-rag.streamlit.app](https://your-url-here.streamlit.app)

A retrieval-augmented generation chatbot that answers natural language questions about Juniper EX and QFX series switches using real datasheet content.

## Stack
- Claude API (Anthropic) — LLM for grounded answers
- sentence-transformers — local embeddings, no API key needed
- ChromaDB — local vector database
- Streamlit — chat UI
- PyMuPDF — PDF text extraction

## Setup
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip3 install -r requirements.txt`
4. Set your Anthropic API key: `export ANTHROPIC_API_KEY="sk-ant-..."`
5. Add Juniper datasheets as PDFs to `datasheets/EX/` and `datasheets/QFX/`
6. Run `python3 ingest.py` to build the knowledge base
7. Run `streamlit run app.py` to launch the chat UI

## How it works
1. Datasheets are chunked into segments and embedded locally using sentence-transformers
2. User questions are embedded using the same model
3. ChromaDB finds the most semantically relevant chunks
4. Claude answers using only the retrieved context — no hallucinated specs
