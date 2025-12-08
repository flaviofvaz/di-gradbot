from backend.src.ingestion.chunking import MarkdownChunker
from backend.src.ingestion.extraction import DoclingExtractor
import asyncio
import uuid


async def main():
    source = "../ingestion/data/Regulamento-PG-DI-2022-12-06.pdf"

    extractor = DoclingExtractor()
    result = await extractor.extract_text(source)
    assert type(result) == str, "Extraction not successful. Output type is not a string"

    chunker = MarkdownChunker()
    chunks = await chunker.chunk_text(result, uuid.uuid4(), source.split("/")[-1])

    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx}:")
        print(chunk.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
