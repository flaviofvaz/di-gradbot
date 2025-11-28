from chunking import BaseChunker
from extraction import BaseExtractor
from ..database.vector import VectorDatabase
from typing import List

class Indexer:
    def __init__(self, extractor: BaseExtractor, chunker: BaseChunker, vector_db: VectorDatabase):
        self._extractor = extractor
        self._chunker = chunker
        self._vector_db = VectorDatabase

    def ingest(self, file_paths: List[str]):