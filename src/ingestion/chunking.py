from chonkie import Pipeline, Document
from abc import ABC, abstractmethod


class BaseChunker(ABC):
    @abstractmethod
    def chunk_text(self, document_text: str) -> str:
        pass


class MarkdownChunker(BaseChunker):
    def __init__(self, recursive_size: int = 2048, semantic_size: int | None = None, overlap: int | None = None):
        pipe = Pipeline().chunk_with(
            "recursive",
            tokenizer="gpt2",
            chunk_size=recursive_size,
            recipe="markdown"
        )
        if semantic_size is not None:
            pipe = pipe.chunk_with("semantic", chunk_size=semantic_size)
        if overlap is not None:
            pipe = pipe.refine_with("overlap", context_size=overlap)

        self._pipeline = pipe
    def chunk_text(self, document_text: str | list[str]) -> Document | list[Document]:
        docs = self._pipeline.run(texts=document_text)
        return docs
    