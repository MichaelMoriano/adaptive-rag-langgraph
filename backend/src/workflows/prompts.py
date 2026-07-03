from langchain_core.prompts import ChatPromptTemplate

# ── Router ──────────────────────────────────────────────────────────────
ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto en decidir si una pregunta debe responderse
con documentos de una base de conocimiento (vectorstore) o con una búsqueda web.

La base de conocimiento contiene documentos sobre: inteligencia artificial,
machine learning, LangGraph y agentes de IA.

Usa 'vectorstore' para preguntas sobre esos temas.
Usa 'web_search' para cualquier otro tema o información reciente."""),
    ("human", "{question}"),
])

# ── Retrieval Grader ─────────────────────────────────────────────────────
GRADER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un evaluador de relevancia de documentos.
Evalúa si el documento recuperado es relevante para la pregunta del usuario.
Si contiene palabras clave o significado semántico relacionado, es relevante.
Responde solo 'yes' o 'no'."""),
    ("human", "Documento: \n\n{document}\n\nPregunta: {question}"),
])

# ── Generation ───────────────────────────────────────────────────────────
GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un asistente de preguntas y respuestas.
Usa ÚNICAMENTE el contexto proporcionado para responder.
Si no sabes la respuesta, dilo claramente.
Máximo 3 oraciones, sé conciso y preciso."""),
    ("human", "Pregunta: {question}\n\nContexto: {context}"),
])

# ── Hallucination Grader ──────────────────────────────────────────────────
HALLUCINATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un evaluador de alucinaciones.
Determina si la respuesta generada está fundamentada en los hechos proporcionados.
Responde solo 'yes' (fundamentada) o 'no' (alucinación)."""),
    ("human", "Hechos: \n\n{documents}\n\nRespuesta generada: {generation}"),
])

# ── Answer Grader ─────────────────────────────────────────────────────────
ANSWER_GRADER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un evaluador de calidad de respuestas.
Determina si la respuesta resuelve la pregunta del usuario.
Responde solo 'yes' (resuelve) o 'no' (no resuelve)."""),
    ("human", "Pregunta: {question}\n\nRespuesta: {generation}"),
])

# ── Query Rewriter ────────────────────────────────────────────────────────
REWRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un optimizador de consultas de búsqueda.
Reescribe la pregunta para mejorar la recuperación de documentos relevantes.
Mantén la intención original pero usa términos más precisos."""),
    ("human", "Pregunta original: {question}\n\nFormula una pregunta mejorada:"),
])