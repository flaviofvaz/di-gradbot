from abc import ABC, abstractmethod
from typing import List

from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os


class BaseEmbedder(ABC):
    """
        Abstract Base Class (ABC) defining the required interface for a text embedding service.

        An embedder converts human-readable text (strings) into dense vector representations
        (lists of floats) that capture semantic meaning.
    """
    @abstractmethod
    async def embed(self, texts: List[str], is_query: bool) -> List[List[float]]:
        """
            Asynchronously generates vector embeddings for a list of text strings.
            Args:
                texts (List[str]): The list of text strings to be embedded.
                is_query (bool): A flag indicating if the texts are being embedded for a
                                 query (search) or for insertion (documents). Some models
                                 use different strategies for queries and documents.
            Returns:
                List[List[float]]: A list of embeddings, where each embedding is a list of floats.
        """
        pass


class SentenceTransformerEmbedder(BaseEmbedder):
    """
        Concrete implementation of BaseEmbedder using a local Sentence Transformer model.
        This class performs embedding operations locally without needing an external API.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
            Initializes the Sentence Transformer model.
            Args:
                model_name (str, optional): The name of the Hugging Face model to load.
                                            Defaults to 'sentence-transformers/all-MiniLM-L6-v2'.
        """
        self._model = SentenceTransformer(model_name)
    async def embed(self, texts: List[str], is_query: bool) -> List[List[float]]:
        """
            Generates embeddings using the loaded Sentence Transformer model.
            It utilizes specialized `encode_query` or `encode_document` methods based
            on the `is_query` flag for optimal performance with certain models.
            Args:
                texts (List[str]): The list of text strings to be embedded.
                is_query (bool): If True, uses the query encoding method; otherwise, uses
                                 the document encoding method.
            Returns:
                List[List[float]]: A list of vector embeddings.
        """
        if is_query:
            embeddings = self._model.encode_query(texts)
        else:
            embeddings = self._model.encode_document(texts)
        return embeddings.tolist()


class OpenAiEmbedder(BaseEmbedder):
    """
        Concrete implementation of BaseEmbedder using the OpenAI API.
        This relies on the 'openai' package and requires the OPENAI_API_KEY environment variable.
    """
    def __init__(self, model_name: str = "text-embedding-3-small"):
        """
            Initializes the OpenAI client and checks for the API key.
            Args:
                model_name (str, optional): The name of the OpenAI embedding model to use.
                                            Defaults to 'text-embedding-3-small'.
            Raises:
                EnvironmentError: If the 'OPENAI_API_KEY' environment variable is not set.
        """
        if os.environ.get("OPENAI_API_KEY") is None:
            raise EnvironmentError("OpenAI API key not set")
        self._client = OpenAI()
        self._model_name = model_name

    async def embed(self, texts: List[str], is_query: bool) -> List[List[float]]:
        """
            Generates embeddings by calling the OpenAI embeddings API endpoint.
            Note: OpenAI's official embedding models do not currently differentiate their
            vector generation based on the `is_query` flag, but the parameter is kept
            for compliance with the `BaseEmbedder` interface.
            Args:
                texts (List[str]): The list of text strings to be embedded.
                is_query (bool): Flag ignored by the current OpenAI implementation, but required by the ABC.
            Returns:
                List[List[float]]: A list of vector embeddings received from the API.
        """
        response = self._client.embeddings.create(
            input=texts,
            model=self._model_name
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
