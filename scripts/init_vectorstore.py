"""
Script para cargar documentos de ejemplo en ChromaDB.
Ejecutar una vez antes de iniciar el sistema: python scripts/init_vectorstore.py
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.llm import get_vectorstore

URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

def main():
    print("Cargando documentos...")
    loader = WebBaseLoader(URLS)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    print(f"  → {len(splits)} chunks creados")

    print("Indexando en ChromaDB...")
    vectorstore = get_vectorstore()
    vectorstore.add_documents(splits)
    print("  → ¡Listo! Vectorstore inicializado.")

if __name__ == "__main__":
    main()