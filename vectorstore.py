from typing import List, Optional
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )


def build_vectorstore(
    client: QdrantClient,
    collection_name: str,
    embeddings,
    texts: List[str],
    metadatas: Optional[List[dict]] = None,
) -> Qdrant:

    vs = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )
    vs.add_texts(texts, metadatas)
    return vs


def ensure_chunks(docs: List[Document], chunk_size: int = 800, chunk_overlap: int = 120) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)
