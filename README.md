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
