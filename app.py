import streamlit as st
import os
from dotenv import load_dotenv

from llm import get_embeddings
from vectorstore import get_qdrant_client, build_vectorstore, ensure_chunks
from pdf_loader import load_pdf
from graph import build_graph

load_dotenv()

st.set_page_config(
    page_title="LangGraph Smart Query Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("LangGraph Smart Query Agent")
st.markdown("<h5 style='color: gray;'>Docs + Weather Smart Assistant</h5>", unsafe_allow_html=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OWM_API_KEY = os.getenv("OWM_API_KEY")
COLLECTION = os.getenv("COLLECTION", "pdf-knowledge")

if "qdrant_client" not in st.session_state:
    st.session_state["qdrant_client"] = get_qdrant_client()
if "uploading" not in st.session_state:
    st.session_state["uploading"] = False
if "graph" not in st.session_state:
    class Dummy:
        def invoke(self, _):
            return []
    st.session_state["graph"] = build_graph(Dummy(), weather_api_key=OWM_API_KEY)

client = st.session_state["qdrant_client"]

with st.sidebar:
    st.subheader("📄 PDF Uploader")
    k = st.number_input("Top K", min_value=1, max_value=15, value=4)
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if st.button("Upload PDF"):
        if not GROQ_API_KEY:
            st.error("Missing GROQ_API_KEY in .env")
        elif not pdf_file:
            st.error("Upload a PDF first")
        else:
            st.session_state["uploading"] = True
            st.session_state["upload_success"] = False
            st.rerun()

if st.session_state["uploading"]:
    st.info("⏳ Uploading and processing your PDF... Please wait.")
    progress_text = st.empty()
    progress_bar = st.progress(0)

    pdf_path = os.path.join(os.getcwd(), "upload.pdf")

    with st.spinner("Processing your PDF..."):
        # Step 1: Save file
        progress_text.text("Saving file...")
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        progress_bar.progress(20)

        # Step 2: Load and chunk
        progress_text.text("Loading and chunking PDF...")
        docs = load_pdf(pdf_path)
        chunks = ensure_chunks(docs)
        texts = [d.page_content for d in chunks]
        progress_bar.progress(50)

        # Step 3: Embeddings + vector store
        progress_text.text("Creating embeddings and vector store...")
        embeddings = get_embeddings()
        vs = build_vectorstore(client, COLLECTION, embeddings, texts)
        progress_bar.progress(80)

        # Step 4: Build graph
        progress_text.text("Building LangGraph...")
        st.session_state["retriever"] = vs.as_retriever(search_kwargs={"k": int(k)})
        st.session_state["vs"] = vs
        st.session_state["graph"] = build_graph(
            st.session_state["retriever"],
            weather_api_key=OWM_API_KEY
        )
        progress_bar.progress(100)

    # --- Success info before rerun ---
    st.session_state["uploading"] = False
    st.session_state["upload_success"] = True
    st.session_state["chunks_indexed"] = len(texts)
    st.session_state["collection_name"] = COLLECTION

    st.rerun()

# --- Show success message after rerun ---
if st.session_state.get("upload_success"):
    st.success(
        f"✅ Upload successful! Indexed **{st.session_state['chunks_indexed']}** chunks "
        f"into **'{st.session_state['collection_name']}'**."
    )
    # clear after display
    st.session_state["upload_success"] = False

# --- Chat UI ---
st.chat_message("assistant").write(
    "Upload a PDF → then ask about it. Or try: **What's the weather in Bengaluru today?** 🌦️"
)

if not st.session_state["uploading"]:
    user_query = st.chat_input("Ask something...")
else:
    user_query = None

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
        st.chat_message("assistant").write(res.get("answer", "(no answer)"))
