import uuid
from typing import List, Optional
from pydantic import BaseModel


class DataPoint(BaseModel):
    """
        Represents a single atomic unit of data stored in the vector database index.

        A DataPoint contains the vector embedding itself along with all necessary
        metadata (IDs, source information) required to locate and contextualize the
        chunk of text from which the vector was generated.
    """
    """A unique identifier for this specific chunk/data point."""
    id: uuid.UUID
    """The unique identifier for the source document from which this chunk was derived."""
    document_id: uuid.UUID
    """The human-readable name of the source document."""
    document_name: str
    """The actual segment (chunk) of text that was used to generate the vector."""
    chunk_text: str
    """
        The dense vector embedding corresponding to the 'chunk_text'. 
        This is typically None until the embedding process is completed.
    """
    vector: Optional[List[float]]
