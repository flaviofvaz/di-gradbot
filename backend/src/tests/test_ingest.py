from backend.src.ingestion.chunking import MarkdownChunker
from backend.src.ingestion.extraction import DoclingExtractor
from backend.src.ingestion.ingest import IndexManager
from backend.src.ingestion.embeddings import OpenAiEmbedder
from backend.src.ingestion.vector_db import QdrantVectorDatabase
import uuid
import asyncio


async def main():
    collection_name = "collection_collection"

    db_client = QdrantVectorDatabase(url="localhost:6333")
    files = [
        ("../ingestion/data/Edital-PG-INF-2025.2.pdf", uuid.uuid4()),
        ("../ingestion/data/Edital_PIPD.pdf", uuid.uuid4()),
        ("../ingestion/data/Regulamento-PG-DI-2022-12-06.pdf", uuid.uuid4())
    ]
    extractor = DoclingExtractor()
    chunker = MarkdownChunker()
    embedder = OpenAiEmbedder()
    vector_db = QdrantVectorDatabase(url="localhost:6333")

    index_manager = IndexManager(extractor=extractor, chunker=chunker, embedder=embedder, vector_db=vector_db, collection_name=collection_name)

    status = await index_manager.insert(files)
    print(status)

    unique_documents = await index_manager.list_stored_files()
    print(unique_documents)

    await db_client.delete_collection(collection_name)

if __name__ == "__main__":
    asyncio.run(main())