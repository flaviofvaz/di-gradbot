from backend.src.ingestion.embeddings import SentenceTransformerEmbedder, OpenAiEmbedder
import asyncio


async def main():
    sentence_embedder = SentenceTransformerEmbedder()
    openai_embedder = OpenAiEmbedder()

    documents = [
        "Venus is often called Earth's twin because of its similar size and proximity.",
        "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
        "Jupiter, the largest planet in our solar system, has a prominent red spot.",
        "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
    ]

    embeddings_st_as_query = await sentence_embedder.embed(documents, is_query=True)
    embeddings_st_as_document = await sentence_embedder.embed(documents, is_query=False)

    # is_query flag is irrelevant for this model
    embeddings_openai = await openai_embedder.embed(documents, is_query=True)

    print(embeddings_st_as_query)
    print(embeddings_st_as_document)
    print(embeddings_openai)


if __name__ == "__main__":
    asyncio.run(main())
