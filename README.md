# Adaptive RAG con LangGraph 🤖

Sistema de **Retrieval-Augmented Generation Adaptativo** construido con LangGraph, OpenAI, Google GenAI y Tavily. El agente decide dinámicamente si responder con documentos indexados o realizar una búsqueda web en tiempo real.

## ¿Qué hace este sistema?

A diferencia de un RAG tradicional que siempre recupera documentos del mismo lugar, este sistema **adapta su estrategia** según la pregunta:

1. **Router** — analiza la pregunta y decide: ¿base de conocimiento o búsqueda web?
2. **Retriever** — recupera documentos relevantes de ChromaDB
3. **Grader** — evalúa si los documentos son realmente útiles
4. **Transform Query** — si no hay documentos útiles, reescribe la pregunta
5. **Generator** — genera la respuesta con el contexto disponible
6. **Hallucination Check** — verifica que la respuesta esté fundamentada en hechos

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   docker-compose                     │
│                                                     │
│  ┌──────────────────┐    ┌──────────────────────┐  │
│  │   UI (Chainlit)  │───▶│  Backend (FastAPI)   │  │
│  │   puerto: 8501   │    │   puerto: 8000       │  │
│  └──────────────────┘    └──────────┬───────────┘  │
│                                     │               │
│                          ┌──────────▼───────────┐  │
│                          │   LangGraph Agent    │  │
│                          │  ChromaDB + Tavily   │  │
│                          └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Orquestación del agente | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OPEN AI |
| Base de datos vectorial | ChromaDB |
| Búsqueda web | Tavily |
| Backend API | FastAPI |
| Frontend | Chainlit |
| Contenedores | Docker + Docker Compose |
| Gestor de paquetes | uv |

## Estructura del proyecto

```
adaptive-rag-langgraph/
├── backend/                    # Servicio FastAPI + LangGraph
│   ├── src/
│   │   ├── api/routes/         # Endpoints REST
│   │   ├── core/               # Config, LLM, embeddings
│   │   ├── schemas/            # Modelos Pydantic
│   │   └── workflows/          # Lógica del agente RAG
│   │       ├── state.py        # Estado del grafo
│   │       ├── prompts.py      # Plantillas de prompts
│   │       ├── chains.py       # Chains con outputs estructurados
│   │       ├── nodes.py        # Nodos del grafo
│   │       ├── routes.py       # Edges condicionales
│   │       └── graph.py        # Ensamblaje del StateGraph
│   └── Dockerfile
├── ui/                         # Interfaz Chainlit
│   ├── src/rag_ui/app.py       # Chat UI
│   └── Dockerfile
├── notebooks/                  # Notebook original de referencia
├── scripts/
│   └── init_vectorstore.py     # Carga inicial de documentos
├── docker-compose.yml
└── .env.example
```

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Cuentas y API keys en:
  - [OpenAI](https://platform.openai.com/) → `OPENAI_API_KEY`
  - [Tavily](https://tavily.com/) → `TAVILY_API_KEY`
  - [Google AI Studio](https://aistudio.google.com/) → `GOOGLE_API_KEY`

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/MichaelMoriano/adaptive-rag-langgraph
cd adaptive-rag-langgraph
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus API keys:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
GOOGLE_API_KEY=AI...
```

### 3. Inicializar la base de conocimiento

```bash
cd backend
pip install uv
uv pip install -e .
cd ..
python scripts/init_vectorstore.py
```

### 4. Levantar los servicios

```bash
docker compose up --build
```

### 5. Abrir la interfaz

| Servicio | URL |
|---|---|
| Chat UI (Chainlit) | http://localhost:8501 |
| API Backend (FastAPI) | http://localhost:8000 |
| Documentación API | http://localhost:8000/docs |

## Uso de la API

### Hacer una pregunta

```bash
curl -X POST http://localhost:8000/api/v1/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué es un agente de IA?"}'
```

Respuesta:

```json
{
  "question": "¿Qué es un agente de IA?",
  "answer": "Un agente de IA es un sistema que...",
  "source": "vectorstore",
  "used_web_search": false,
  "rewritten_question": null
}
```

### Health check

```bash
curl http://localhost:8000/api/v1/health
```

## Flujo del agente (paso a paso)

```
Pregunta del usuario
        │
        ▼
   [Router] ──────────────────────────────────────┐
        │ vectorstore                         web_search
        ▼                                         ▼
   [Retrieve]                             [Web Search]
        │                                         │
        ▼                                         │
[Grade Documents]                                 │
        │                                         │
   relevantes ──────────────────────────────────▶ │
        │ no relevantes                           │
        ▼                                         │
[Transform Query]                                 │
        │                                         │
        └──────────────────┬──────────────────────┘
                           ▼
                      [Generate]
                           │
                           ▼
               [Hallucination Check]
                  /              \
            alucinación        fundamentada
                │                    │
          [Generate] (retry)    [Answer Grade]
                               /            \
                          no útil          útil
                              │               │
                    [Transform Query]        END
```

## Referencia del artículo

Este proyecto está basado en:
> [Building an Adaptive RAG System with LangGraph, OpenAI, and Tavily](https://levelup.gitconnected.com/building-an-adaptive-rag-system-with-langgraph-openai-and-tavily-c4ee39d2f021)

El notebook original del artículo está disponible en [`notebooks/RAG.ipynb`](notebooks/RAG.ipynb).

## Recursos relacionados

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Adaptive RAG Paper](https://arxiv.org/abs/2403.14403)
- [Corrective RAG Paper](https://arxiv.org/abs/2401.15884)