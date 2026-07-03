import httpx
import chainlit as cl
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="👋 Hola! Soy tu asistente de **Adaptive RAG**.\n\n"
                "Puedo responder preguntas sobre IA y LangGraph usando documentos indexados, "
                "y cuando no tenga información, buscaré en la web automáticamente.\n\n"
                "¿Qué deseas saber?"
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    async with cl.Step(name="Consultando al agente RAG...") as step:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/v1/rag/ask",
                    json={"question": message.content},
                )
                response.raise_for_status()
                data = response.json()

            source_emoji = "🌐" if data["used_web_search"] else "📚"
            source_label = "búsqueda web" if data["used_web_search"] else "base de conocimiento"
            step.output = f"Fuente: {source_emoji} {source_label}"

            content = data["answer"]
            if data.get("rewritten_question"):
                content += f"\n\n> 💡 *Pregunta optimizada: \"{data['rewritten_question']}\"*"

            await cl.Message(content=content).send()

        except httpx.HTTPError as e:
            await cl.Message(content=f"❌ Error conectando al backend: {e}").send()