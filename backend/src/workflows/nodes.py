from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document

from src.workflows.state import GraphState
from src.workflows.chains import (
    retrieval_grader_chain,
    generation_chain,
    question_rewriter_chain,
)
from src.core.llm import get_retriever

retriever = get_retriever()
web_search_tool = TavilySearchResults(max_results=3)


def retrieve(state: GraphState) -> GraphState:
    """Nodo: recupera documentos del vectorstore."""
    print("── Nodo: RETRIEVE")
    documents = retriever.invoke(state["question"])
    return {"documents": documents}


def web_search(state: GraphState) -> GraphState:
    """Nodo: busca en la web con Tavily."""
    print("── Nodo: WEB SEARCH")
    results = web_search_tool.invoke({"query": state["question"]})
    content = "\n\n".join([r["content"] for r in results])
    web_doc = Document(page_content=content)
    return {"documents": [web_doc], "web_search_needed": "Yes"}


def grade_documents(state: GraphState) -> GraphState:
    """Nodo: filtra documentos no relevantes y decide si necesita web search."""
    print("── Nodo: GRADE DOCUMENTS")
    filtered_docs = []
    web_search_needed = "No"

    for doc in state["documents"]:
        score = retrieval_grader_chain.invoke({
            "question": state["question"],
            "document": doc.page_content,
        })
        if score.binary_score == "yes":
            filtered_docs.append(doc)
        else:
            web_search_needed = "Yes"

    return {"documents": filtered_docs, "web_search_needed": web_search_needed}


def generate(state: GraphState) -> GraphState:
    """Nodo: genera respuesta con los documentos disponibles."""
    print("── Nodo: GENERATE")
    context = "\n\n".join([doc.page_content for doc in state["documents"]])
    generation = generation_chain.invoke({
        "question": state["question"],
        "context": context,
    })
    retry_count = state.get("retry_count", 0) + 1
    return {"generation": generation, "retry_count": retry_count}


def transform_query(state: GraphState) -> GraphState:
    """Nodo: reescribe la pregunta para mejor recuperación."""
    print("── Nodo: TRANSFORM QUERY")
    better_question = question_rewriter_chain.invoke({"question": state["question"]})
    return {"question": better_question}