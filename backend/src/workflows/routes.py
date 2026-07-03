from src.workflows.state import GraphState
from src.workflows.chains import router_chain, hallucination_grader_chain, answer_grader_chain


def route_question(state: GraphState) -> str:
    """Edge condicional: decide si ir a vectorstore o web_search."""
    print("── Edge: ROUTE QUESTION")
    source = router_chain.invoke({"question": state["question"]})
    print(f"   → Routing a: {source.datasource}")
    return source.datasource  # "vectorstore" o "web_search"


def decide_to_generate(state: GraphState) -> str:
    """Edge condicional: genera o transforma la query."""
    print("── Edge: DECIDE TO GENERATE")
    if state["web_search_needed"] == "Yes":
        print("   → Transformando query")
        return "transform_query"
    print("   → Generando respuesta")
    return "generate"


def grade_generation(state: GraphState) -> str:
    """Edge condicional: valida la respuesta con límite de reintentos."""
    print("── Edge: GRADE GENERATION")

    retry_count = state.get("retry_count", 0)
    if retry_count >= 2:
        print("   → Límite de reintentos alcanzado, forzando respuesta útil")
        return "useful"

    hallucination_score = hallucination_grader_chain.invoke({
        "documents": state["documents"],
        "generation": state["generation"],
    })

    if hallucination_score.binary_score == "no":
        print("   → Alucinación detectada, regenerando")
        return "not supported"

    answer_score = answer_grader_chain.invoke({
        "question": state["question"],
        "generation": state["generation"],
    })

    if answer_score.binary_score == "yes":
        print("   → Respuesta útil ✓")
        return "useful"

    print("   → Respuesta no útil, transformando query")
    return "not useful"