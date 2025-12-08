from backend.src.ingestion.embeddings import OpenAiEmbedder
from backend.src.ingestion.vector_db import QdrantVectorDatabase
from backend.src.llm import OpenAiLlm
from backend.src.chatbot import ChatBot
import asyncio


async def main():
    collection_name = "grad_documents"
    embedder = OpenAiEmbedder()
    vector_db = QdrantVectorDatabase(url="http://localhost:6333")
    llm = OpenAiLlm()
    chat_bot = ChatBot(embedder=embedder, vector_db=vector_db, llm=llm, collection_name=collection_name)

    msg = await chat_bot.interact([{"role": "user", "content": "em qual período é recomendado que eu faça o exame de proficiência em inglês?"}])
    print(msg)

if __name__ == "__main__":
    asyncio.run(main())

