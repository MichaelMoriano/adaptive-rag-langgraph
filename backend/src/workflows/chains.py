from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

from src.core.llm import get_llm
from src.workflows.prompts import (
    ROUTER_PROMPT,
    GRADER_PROMPT,
    GENERATION_PROMPT,
    HALLUCINATION_PROMPT,
    ANSWER_GRADER_PROMPT,
    REWRITER_PROMPT,
)

llm = get_llm()


# ── Structured Output Schemas ─────────────────────────────────────────────
class RouteQuery(BaseModel):
    """Decisión de routing: vectorstore o web_search."""
    datasource: str = Field(description="'vectorstore' o 'web_search'")


class GradeDocuments(BaseModel):
    """Evaluación de relevancia de documento."""
    binary_score: str = Field(description="'yes' si es relevante, 'no' si no")


class GradeHallucinations(BaseModel):
    """Evaluación de alucinaciones en la respuesta."""
    binary_score: str = Field(description="'yes' si está fundamentada, 'no' si alucina")


class GradeAnswer(BaseModel):
    """Evaluación de utilidad de la respuesta."""
    binary_score: str = Field(description="'yes' si resuelve la pregunta, 'no' si no")


# ── Chains ────────────────────────────────────────────────────────────────
router_chain = ROUTER_PROMPT | llm.with_structured_output(RouteQuery)

retrieval_grader_chain = GRADER_PROMPT | llm.with_structured_output(GradeDocuments)

generation_chain = GENERATION_PROMPT | llm | StrOutputParser()

hallucination_grader_chain = HALLUCINATION_PROMPT | llm.with_structured_output(GradeHallucinations)

answer_grader_chain = ANSWER_GRADER_PROMPT | llm.with_structured_output(GradeAnswer)

question_rewriter_chain = REWRITER_PROMPT | llm | StrOutputParser()