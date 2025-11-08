from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import os

def load_pdf(path: str) -> List[Document]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")
    loader = PyPDFLoader(path)
    return loader.load()
