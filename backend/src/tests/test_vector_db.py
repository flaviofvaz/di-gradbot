from backend.src.ingestion.vector_db import QdrantVectorDatabase
from backend.src.ingestion.data_models import DataPoint
import asyncio
import uuid


async def main():
    collection_name = "collection_collection"
    db_client = QdrantVectorDatabase(url="localhost:6333")
    db_client.create_collection(collection_name, vector_field_dimension=4)

    document_id_1 = uuid.uuid4()
    document_id_2 = uuid.uuid4()
    document_id_3 = uuid.uuid4()
    document_name = "test_document"

    operation_info = await db_client.insert(
        collection_name=collection_name,
        data_points=[
            DataPoint(id=uuid.uuid4(), document_id=document_id_1, document_name=document_name, chunk_text="a", vector=[0.05, 0.61, 0.76, 0.74]),
            DataPoint(id=uuid.uuid4(), document_id=document_id_2, document_name=document_name, chunk_text="b", vector=[0.19, 0.81, 0.75, 0.11]),
            DataPoint(id=uuid.uuid4(), document_id=document_id_3, document_name=document_name, chunk_text="c", vector=[0.36, 0.55, 0.47, 0.94]),
            DataPoint(id=uuid.uuid4(), document_id=document_id_1, document_name=document_name, chunk_text="d", vector=[0.18, 0.01, 0.85, 0.80]),
            DataPoint(id=uuid.uuid4(), document_id=document_id_2, document_name=document_name, chunk_text="e", vector=[0.24, 0.18, 0.22, 0.44]),
            DataPoint(id=uuid.uuid4(), document_id=document_id_3, document_name=document_name, chunk_text="f", vector=[0.35, 0.08, 0.11, 0.44]),
        ],
    )
    assert operation_info, "Points not uploaded to Qdrant collection"

    search_results = await db_client.retrieve(
        collection_name=collection_name,
        query_vector=[0.2, 0.1, 0.9, 0.7],
    )
    print(search_results)

    unique_documents = await db_client.list_unique_documents(collection_name=collection_name)
    print(unique_documents)

    await db_client.remove(collection_name=collection_name , document_name=document_name)
    await db_client.delete_collection(collection_name)

if __name__ == "__main__":
    asyncio.run(main())
