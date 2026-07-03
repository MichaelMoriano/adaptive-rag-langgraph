from langgraph.graph import StateGraph, START, END

from src.workflows.state import GraphState
from src.workflows.nodes import retrieve, web_search, grade_documents, generate, transform_query
from src.workflows.routes import route_question, decide_to_generate, grade_generation


def build_graph() -> StateGraph:
    """Construye y compila el grafo Adaptive RAG."""
    graph = StateGraph(GraphState)

    # ── Registrar nodos ───────────────────────────────────────────────────
    graph.add_node("retrieve", retrieve)
    graph.add_node("web_search", web_search)
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("generate", generate)
    graph.add_node("transform_query", transform_query)

    # ── Edges desde el inicio ─────────────────────────────────────────────
    graph.add_conditional_edges(
        START,
        route_question,
        {
            "vectorstore": "retrieve",
            "web_search": "web_search",
        },
    )

    # ── Edges fijos ───────────────────────────────────────────────────────
    graph.add_edge("retrieve", "grade_documents")
    graph.add_edge("web_search", "generate")
    graph.add_edge("transform_query", "retrieve")

    # ── Edges condicionales ───────────────────────────────────────────────
    graph.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )

    graph.add_conditional_edges(
        "generate",
        grade_generation,
        {
            "not supported": "generate",   # regenera si hay alucinación
            "useful": END,
            "not useful": "transform_query",
        },
    )

    return graph.compile()


# Instancia compilada — importable directamente
adaptive_rag_graph = build_graph()