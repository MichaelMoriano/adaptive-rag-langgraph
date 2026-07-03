from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.core.config import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    """Singleton LLM instance."""
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )


@lru_cache(maxsize=1)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Singleton embeddings instance."""
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    """Singleton ChromaDB instance."""
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=get_embeddings(),
    )


def get_retriever():
    return get_vectorstore().as_retriever(search_kwargs={"k": 3})