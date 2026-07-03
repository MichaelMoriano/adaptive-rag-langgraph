from fastapi import APIRouter, HTTPException
from src.schemas.rag import QuestionRequest, RAGResponse
from src.workflows.graph import adaptive_rag_graph

router = APIRouter()


@router.post("/ask", response_model=RAGResponse, tags=["rag"])
async def ask_question(request: QuestionRequest):
    """Endpoint principal: recibe una pregunta y devuelve la respuesta del agente RAG."""
    try:
        result = adaptive_rag_graph.invoke({
            "question": request.question,
            "original_question": request.question,
            "generation": "",
            "web_search_needed": "No",
            "documents": [],
        })

        return RAGResponse(
            question=request.question,
            answer=result["generation"],
            source="web_search" if result.get("web_search_needed") == "Yes" else "vectorstore",
            used_web_search=result.get("web_search_needed") == "Yes",
            rewritten_question=result["question"] if result["question"] != request.question else None,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))