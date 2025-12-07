from .chunking import BaseChunker
from .extraction import BaseExtractor
from .vector_db import BaseVectorDatabase
from .embeddings import BaseEmbedder
from typing import List, Tuple
import uuid


class IndexManager:
    """
        Manages the end-to-end process of indexing documents into a vector database.

        This class orchestrates the pipeline involving text extraction, chunking,
        embedding generation, and storage in a vector database.
    """
    def __init__(self, extractor: BaseExtractor, chunker: BaseChunker, embedder: BaseEmbedder, vector_db: BaseVectorDatabase, collection_name: str):
        """
            Initializes the IndexManager with all required service dependencies.
            It also ensures the target vector collection is created if it does not already exist,
            using a default vector dimension of 1536.
            Args:
                extractor (BaseExtractor): The service responsible for extracting text from files.
                chunker (BaseChunker): The service responsible for splitting text into manageable chunks (DataPoints).
                embedder (BaseEmbedder): The service responsible for generating vector embeddings from text.
                vector_db (BaseVectorDatabase): The service responsible for storing and retrieving vectors.
                collection_name (str): The name of the collection/index in the vector database to use.
        """
        self._extractor = extractor
        self._chunker = chunker
        self._embedder = embedder
        self._vector_db = vector_db
        self._collection_name = collection_name

        # create collection if it doesn't already exist
        exists = self._vector_db.collection_exists(self._collection_name)
        if not exists:
            self._vector_db.create_collection(self._collection_name, vector_field_dimension=1536)

    async def insert(self, file_paths: List[Tuple[str, uuid.UUID]]) -> List[bool]:
        """
            Processes and indexes documents from a list of file paths into the vector database.
            The indexing pipeline performs the following steps for each file:
            1. Extract text (e.g., from PDF to Markdown).
            2. Chunk the text into DataPoints.
            3. Generate vector embeddings for all chunk texts.
            4. Assign the generated vectors to the DataPoints.
            5. Insert the DataPoints (vectors and metadata) into the vector database.
            Args:
                file_paths (List[Tuple[str, uuid.UUID]]): A list where each element is a tuple
                                                          containing the file path and its associated UUID.
            Returns:
                List[bool]: A list of booleans indicating the success status for each corresponding file in the input list.
        """
        files_uploaded = [False for _ in range(len(file_paths))]
        for idx, f in enumerate(file_paths):
            file_path = f[0]
            file_id = f[1]

            # extract text from pdf into markdown text
            md_text = await self._extractor.extract_text(file_path)

            # chunk the text
            data_points = await self._chunker.chunk_text(md_text, file_id, file_path.split("/")[-1])

            # get text from chunks
            chunk_texts = [p.chunk_text for p in data_points]

            # embed texts as documents
            embeddings = await self._embedder.embed(chunk_texts, is_query=False)

            # assign vectors to data_points
            for p, e in zip(data_points, embeddings):
                p.vector = e

            # insert data into vector database
            success = await self._vector_db.insert(collection_name=self._collection_name, data_points=data_points)

            # if any document fails to upload, return an error
            if not success:
                break
            files_uploaded[idx] = success
        return files_uploaded

    async def remove(self, file_names: List[str]) -> List[bool]:
        """
            Removes all vectors and associated metadata for a list of documents from the vector database.
            Args:
                file_names (List[str]): A list of document names to be removed.
            Returns:
                List[bool]: A list of booleans indicating the success status for each corresponding file removal.
        """
        files_removed = [False for _ in range(len(file_names))]
        for idx, f in enumerate(file_names):
            success = await self._vector_db.remove(collection_name=self._collection_name, document_name=f)

            # if any document fails to be removed, return an error
            if not success:
                break
            files_removed[idx] = success
        return files_removed

    async def list_stored_files(self) -> List[str]:
        """
            Retrieves a list of all unique document names currently stored in the vector database collection.
            Returns:
                List[str]: A list of unique document names (strings).
        """
        return await self._vector_db.list_unique_documents(collection_name=self._collection_name)