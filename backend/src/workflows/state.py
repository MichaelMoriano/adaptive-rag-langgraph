from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    Estado centralizado del grafo Adaptive RAG.

    Attributes:
        question: Pregunta actual (puede ser reescrita por transform_query)
        generation: Respuesta generada por el LLM
        web_search_needed: Flag "Yes"/"No" — si los docs no son relevantes
        documents: Lista de documentos recuperados (vectorstore o web)
        original_question: Pregunta original del usuario (antes de reescritura)
        retry_count: Contador de reintentos (para evitar bucles infinitos)
    """
    question: str
    generation: str
    web_search_needed: str
    documents: List[Document]
    original_question: str
    retry_count: int