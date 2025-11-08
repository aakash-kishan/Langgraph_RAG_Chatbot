import streamlit as st
import os
from dotenv import load_dotenv

from llm import get_embeddings
from vectorstore import get_qdrant_client, build_vectorstore, ensure_chunks
from pdf_loader import load_pdf
from graph import build_graph

load_dotenv()

st.set_page_config(page_title="LangGraph RAG + Weather (Groq)", page_icon="☁️", layout="wide")
st.title("LangGraph RAG + Weather")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OWM_API_KEY = os.getenv("OWM_API_KEY")
COLLECTION = os.getenv("COLLECTION", "pdf-knowledge")

if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = get_qdrant_client(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

client = st.session_state["qdrant_client"]

with st.sidebar:
    st.subheader("PDF Indexing")
    k = st.number_input("Top K", min_value=1, max_value=15, value=4)

    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if st.button("Index PDF"):
        if not GROQ_API_KEY:
            st.error("Missing GROQ_API_KEY in .env")
        elif not pdf_file:
            st.error("Upload a PDF first")
        else:
            pdf_path = os.path.join(os.getcwd(), "upload.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.read())

            docs = load_pdf(pdf_path)
            chunks = ensure_chunks(docs)
            texts = [d.page_content for d in chunks]

            embeddings = get_embeddings()
            vs = build_vectorstore(client, COLLECTION, embeddings, texts)

            
            st.session_state["retriever"] = vs.as_retriever(search_kwargs={"k": int(k)})
            st.session_state["vs"] = vs
            st.success(f"Indexed {len(texts)} chunks into '{COLLECTION}' ✅")
            st.session_state["graph"] = build_graph(st.session_state["retriever"], weather_api_key=OWM_API_KEY)


if "graph" not in st.session_state:
    retriever = st.session_state.get("retriever")
    if not retriever:
        class Dummy:
            def invoke(self, _):
                return []

        retriever = Dummy()
    st.session_state["graph"] = build_graph(retriever, weather_api_key=OWM_API_KEY)

st.chat_message("assistant").write(
    "Upload a PDF → then ask about it. Try: **What's the weather in Bengaluru today?** 🌦️"
)

user_query = st.chat_input("Ask something...")

if user_query:
    graph = st.session_state["graph"]

    retriever = st.session_state.get("retriever")
    if not retriever:
        class Dummy:
            def invoke(self, _):
                return []

        retriever = Dummy()

    with st.spinner("Thinking..."):
        res = graph.invoke({
            "question": user_query,
            "retriever": retriever
        })

        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(res.get("answer","(no answer)"))
