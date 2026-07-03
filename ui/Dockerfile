FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system chainlit httpx python-dotenv

COPY src/ ./src/
COPY chainlit.md .

EXPOSE 8501

CMD ["chainlit", "run", "src/rag_ui/app.py", "--host", "0.0.0.0", "--port", "8501"]