FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system fastapi uvicorn langchain langgraph langchain-openai langchain-community langchain-chroma langchain-text-splitters tavily-python tiktoken python-dotenv pydantic-settings

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]