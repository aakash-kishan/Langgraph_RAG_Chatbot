# LangGraph Smart Query Agent — LangGraph RAG + Weather AI Assistant

A simple, clean, and production-style demo that combines **LangGraph** (agentic routing), **RAG over PDFs (Qdrant vector DB)**, **real-time weather (OpenWeatherMap)**, and **Groq LLM** — wrapped in a friendly **Streamlit chat UI**.

👉 [**Live Demo**](https://langgraphragchatbot-connect.streamlit.app)


## ✨ What it does

Two tools, one agentic flow (LangGraph):

### 📡 Weather: Fetches real-time weather via OpenWeatherMap.

### 📚 RAG: Answers questions from your uploaded PDF using Qdrant + embeddings.

Router node decides whether a user query is about weather or the document.

Embeddings: sentence-transformers/all-MiniLM-L6-v2 (384-dim).

**LLM:** Groq llama-3.3-70b-versatile (configurable).

**UI**: Streamlit chat with inline PDF upload, progress messages, and guardrails (chat is temporarily disabled while indexing).

**Tests**: Pytest covering routing, synthesis, and API handling.

## 🧱 Tech Stack

**Core:** Python, Streamlit

**Agentic:** LangGraph + LangChain

**LLM:** Groq (Chat Completions)

**RAG:** Qdrant Cloud (vector DB), LangChain Qdrant integration

**Embeddings:** HuggingFace MiniLM (via langchain-community)

**Weather:** OpenWeatherMap REST API

**PDF:** pypdf + langchain-text-splitters

**Tests:** Pytest

## 🚀 Getting Started -Run Locally

1. Clone & enter the project

```bash
git clone https://github.com/aakash-kishan/Langgraph_RAG_Chatbot.git

cd Langgraph_RAG_Chatbot

python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

```
2. Install dependencies

```bash
pip install -r requirements.txt

```
3. Create .env from .env.example and fill your keys

4. Run
```bash

streamlit run app.py

```
## 🔐 Environment Variables

Copy .env.example → .env (local), and paste the same keys (TOML format) in Streamlit Cloud Secrets:

```toml
GROQ_API_KEY = "<your_groq_key>"
OWM_API_KEY = "<your_openweather_key>"

# Optional but recommended for tracing (if you use LangSmith)
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_PROJECT = "langgraph-rag-weather"
LANGSMITH_API_KEY = "<your_langsmith_key>"

# Qdrant Cloud (recommended for deployment)
QDRANT_URL = "https://<your-cluster-id>.aws.cloud.qdrant.io"
QDRANT_API_KEY = "<your_qdrant_api_key>"
COLLECTION = "pdf-knowledge"

```
## ☁️ Deploy on Streamlit Community Cloud

1. Push your repo to GitHub (public).

2. Go to https://share.streamlit.io/

3. New App → pick the repo, branch main, app file app.py.

4. Open Settings → Secrets, paste your keys in TOML:

```toml
GROQ_API_KEY = "..."
OWM_API_KEY = "..."
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_PROJECT = "langgraph-rag-weather"
LANGSMITH_API_KEY = "..."
QDRANT_URL = "https://<cluster>.aws.cloud.qdrant.io"
QDRANT_API_KEY = "..."
COLLECTION = "pdf-knowledge"

```
5. Qdrant Cloud Security → CORS: set Allowed Origins/Headers/Methods to * (or allow your Streamlit app domain).

6. Deploy-done!

## 🧪 Tests

Run all unit tests:

```bash

pytest -q

```

What’s covered:

  - Router: route_llm() correctly classifies weather vs RAG queries (with fallback heuristics).

  - Synthesis: polishing step returns clean text.

  - Weather: API path & error handling (uses fake or missing key to ensure non-crash behavior).

## 🧭 How the Agent Flow Works (LangGraph)

- The router uses a strict JSON prompt. If parsing fails, simple keyword heuristics fall back (e.g., “weather”, “temperature”, “rain”…).

- RAG: your PDF is loaded, chunked, embedded, and stored in Qdrant. A retriever is created and passed into the graph at runtime.

- Synthesis polishes the final answer (short, clear, actionable).

