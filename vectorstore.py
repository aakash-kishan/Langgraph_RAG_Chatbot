# vectorstore.py

import os
from typing import List, Optional
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import VectorParams, Distance


def get_qdrant_client(url: str | None = None, api_key: str | None = None):
    """
    if cloud → pass url + api_key
    if local → leave url=None and connect to local embedded / disk
    """
    if url and url.startswith("http"):
        return QdrantClient(url=url, api_key=api_key)

    # fallback = local embedded
    return QdrantClient(path=".qdrant")

def build_vectorstore(
    client: QdrantClient,
    collection_name: str,
    embeddings,
    texts: List[str],
    metadatas: Optional[List[dict]] = None,
) -> Qdrant:
    # 1) calc embedding dim
    dim = len(embeddings.embed_query("hello"))

    # 2) ensure collection exists
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

    # 3) create langchain wrapper
    vs = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )

    # 4) store text
    vs.add_texts(texts=texts, metadatas=metadatas)
    return vs


def ensure_chunks(docs: List[Document], chunk_size: int = 800, chunk_overlap: int = 120) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)
