from backend.src.ingestion.extraction import DoclingExtractor
import asyncio


async def main():
    source = "../ingestion/data/Regulamento-PG-DI-2022-12-06.pdf"
    extractor = DoclingExtractor()
    result = await extractor.extract_text(source)
    assert type(result) == str, "Extraction not successful. Output type is not a string"
    print(result)

if __name__ == "__main__":
    asyncio.run(main())