# Guía de desarrollo

## Requisitos del entorno

- Python 3.11+
- Docker Desktop
- uv (`pip install uv`)

## Configuración local (sin Docker)

### Backend

```bash
cd backend
uv pip install -e .
uvicorn src.main:app --reload --port 8000
```

### UI

```bash
cd ui
uv pip install -e .
chainlit run src/rag_ui/app.py --port 8501
```

## Variables de entorno

| Variable | Descripción | Requerida |
|---|---|---|
| `OPENAI_API_KEY` | API key de OpenAI | ✅ |
| `TAVILY_API_KEY` | API key de Tavily Search | ✅ |
| `GOOGLE_API_KEY` | API key de Google AI Studio | ✅ |
| `OPENAI_MODEL` | Modelo a usar | ❌ (default: gpt-4o-mini) |
| `BACKEND_URL` | URL del backend para la UI | ❌ (default: http://localhost:8000) |

## Convención de commits

```
feat:     nueva funcionalidad
fix:      corrección de bug
docs:     cambios en documentación
refactor: reorganización sin cambio de comportamiento
chore:    tareas de mantenimiento
```

## Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Health check del servicio |
| POST | `/api/v1/rag/ask` | Enviar pregunta al agente RAG |
| GET | `/docs` | Documentación Swagger UI |