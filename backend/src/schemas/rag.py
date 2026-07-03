from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        description="Pregunta del usuario al sistema RAG",
        min_length=3,
        max_length=500,
    )


class RAGResponse(BaseModel):
    question: str
    answer: str
    source: str = Field(description="'vectorstore' o 'web_search'")
    used_web_search: bool = False
    rewritten_question: str | None = None