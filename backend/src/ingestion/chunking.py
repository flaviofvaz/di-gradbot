from chonkie import Pipeline
from .data_models import DataPoint
from abc import ABC, abstractmethod
from typing import List
import uuid


class BaseChunker(ABC):
    """
        Abstract Base Class (ABC) defining the required interface for a text chunking service.

        A chunker takes a large block of document text and divides it into smaller,
        semantically meaningful segments, each represented as a DataPoint object.
    """
    @abstractmethod
    async def chunk_text(self, document_text: str, document_id: uuid.UUID, document_name: str) -> List[DataPoint]:
        """
            Asynchronously chunks a document's text content into a list of DataPoint objects.
            Args:
                document_text (str): The full text content of the document to be chunked.
                document_id (uuid.UUID): The unique ID of the source document.
                document_name (str): The human-readable name of the source document.
            Returns:
                List[DataPoint]: A list of DataPoint objects, each containing a chunk of text
                                 and the associated metadata.
        """
        pass


class MarkdownChunker(BaseChunker):
    """
        Concrete implementation of BaseChunker using the 'chonkie' library pipeline.
        It is specifically configured to chunk Markdown-formatted text, optionally applying
        semantic chunking and overlap refinement.
    """
    def __init__(self, recursive_size: int = 2048, semantic_size: int | None = None, overlap: int | None = None):
        """
            Initializes and configures the 'chonkie' chunking pipeline.
            The pipeline is built sequentially:
            1. Base: Recursive splitting tailored for Markdown structure, using a tokenizer
               based on 'gpt2' with a configurable `recursive_size`.
            2. Optional: If `semantic_size` is provided, adds a semantic chunking step.
            3. Optional: If `overlap` is provided, adds an overlap refinement step
               to ensure chunks retain context from adjacent segments.
            Args:
                recursive_size (int, optional): The target chunk size for the initial recursive split. Defaults to 2048.
                semantic_size (int | None, optional): The target chunk size for the optional semantic split. Defaults to None.
                overlap (int | None, optional): The size of the context to overlap between refined chunks. Defaults to None.
        """
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


    async def chunk_text(self, document_text: str | list[str], document_id: uuid.UUID, document_name: str) -> List[DataPoint]:
        """
            Runs the text through the configured 'chonkie' pipeline and converts the results
            into a list of DataPoint objects.
            Each resulting chunk text is mapped to a new DataPoint with a unique ID,
            its text content, and the source document's metadata. The vector field is
            initialized as an empty list (to be populated later by the embedder).
            Args:
                document_text (str | list[str]): The text to be chunked.
                document_id (uuid.UUID): The unique ID of the source document.
                document_name (str): The human-readable name of the source document.
            Returns:
                List[DataPoint]: A list of DataPoint objects ready for embedding and indexing.
        """
        docs = self._pipeline.run(texts=document_text)
        data_points = []
        for chunk in docs.chunks:
            data_point = DataPoint(id=uuid.uuid4(), document_id=document_id, document_name=document_name, chunk_text= chunk.text, vector=[])
            data_points.append(
                data_point
            )
        return data_points
    