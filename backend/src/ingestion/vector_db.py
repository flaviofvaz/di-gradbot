from .data_models import DataPoint
from abc import ABC, abstractmethod
from qdrant_client import QdrantClient, models
from typing import List


class BaseVectorDatabase(ABC):
    """
        Abstract Base Class (ABC) defining the required interface for a vector database.
        All concrete vector database implementations must inherit from this class
        and implement all abstract methods.
    """
    @abstractmethod
    async def insert(self, collection_name: str, data_points: List[DataPoint]) -> bool:
        """
            Inserts a list of vector data points into a specified collection.
            Args:
                collection_name (str): The name of the collection to insert into.
                data_points (List[DataPoint]): A list of DataPoint objects to insert.
            Returns:
                bool: True if the insertion was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def retrieve(self, collection_name: str, query_vector: List[float]) -> List[DataPoint]:
        """
            Retrieves the most similar data points to a given query vector.
            Args:
                collection_name (str): The name of the collection to search.
                query_vector (List[float]): The vector used for similarity search.
            Returns:
                List[DataPoint]: A list of retrieved DataPoint objects, ordered by similarity.
        """
        pass

    @abstractmethod
    async def remove(self, collection_name, document_name: str):
        """
            Removes all data points associated with a specific document name from a collection.
            Args:
                collection_name (str): The name of the collection to update.
                document_name (str): The name of the document whose points should be removed.
        """
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, vector_field_dimension: int) -> bool:
        """
            Creates a new collection in the database.
            Args:
                collection_name (str): The name for the new collection.
                vector_field_dimension (int): The dimensionality of the vectors in the collection.
            Returns:
                bool: True if the collection was successfully created.
        """
        pass

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> bool:
        """
            Deletes an entire collection from the database.
            Args:
                collection_name (str): The name of the collection to delete.
            Returns:
                bool: True if the collection was successfully deleted.
        """
        pass

    @abstractmethod
    async def list_unique_documents(self, collection_name: str) -> List[str]:
        """
            Retrieves a list of all unique document names present in a collection.
            Args:
                collection_name (str): The name of the collection to query.
            Returns:
                List[str]: A list of unique document names (strings).
        """
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        """
            Checks if a collection with the given name already exists.
            Args:
                collection_name (str): The name of the collection to check.
            Returns:
                bool: True if the collection exists, False otherwise.
        """
        pass


class QdrantVectorDatabase(BaseVectorDatabase):
    """
        Concrete implementation of BaseVectorDatabase using the Qdrant vector search engine.
    """
    def __init__(self, url: str):
        """
            Initializes the Qdrant client connection.
            Args:
                url (str): The URL of the Qdrant service (e.g., "http://localhost:6333").
        """
        self._client = QdrantClient(url=url)

    async def _create_qdrant_points(self, data_points: List[DataPoint]) -> List[models.PointStruct]:
        """
            Converts custom DataPoint objects into Qdrant-compatible PointStruct objects.
            Args:
                data_points (List[DataPoint]): List of custom data points.
            Returns:
                List[models.PointStruct]: List of points ready for Qdrant insertion.
        """
        qdrant_points = []
        for p in data_points:
            qdrant_points.append(
                models.PointStruct(
                    id=p.id.hex,
                    vector= p.vector,
                    payload=
                    {
                        "chunk_text": p.chunk_text,
                        "document_id": p.document_id.hex,
                        "document_name": p.document_name
                    },
                )
            )
        return qdrant_points

    async def insert(self, collection_name: str, data_points: List[DataPoint]) -> bool:
        """
            Inserts a list of vector data points into a specified Qdrant collection.
            Args:
                collection_name (str): The name of the collection to insert into.
                data_points (List[DataPoint]): A list of DataPoint objects to insert.

            Returns:
                bool: True if the insertion was successful, False otherwise.
        """
        qdrant_points = await self._create_qdrant_points(data_points)
        try:
            self._client.upload_points(
                collection_name=collection_name,
                points=qdrant_points,
                batch_size=10_000,
                wait=True
            )
        except Exception as e:
            print(f"Error occurred while inserting points into qdrant collection {collection_name}. Exception: {str(e)}")
            return False
        print(f"Successfully uploaded points to Qdrant collection {collection_name}")
        return True


    async def retrieve(self, collection_name:str, query_vector: List[float], top_k: int = 3) -> List[DataPoint]:
        """
            Retrieves the top_k most similar data points to a given query vector from Qdrant.
            Args:
                collection_name (str): The name of the collection to search.
                query_vector (List[float]): The vector used for similarity search.
                top_k (int, optional): The number of top results to return. Defaults to 3.
            Returns:
                List[DataPoint]: A list of retrieved Qdrant points (models.ScoredPoint),
                                 which would typically need conversion back to DataPoint objects
                                 for full compliance with the BaseVectorDatabase return type.
        """
        results = self._client.query_points(
            collection_name=collection_name,
            query=query_vector,
            with_payload=True,
            limit=top_k,
        ).points
        return results


    async def remove(self, collection_name: str, document_name: str):
        """
            Removes all data points associated with a specific document name using a filter.
            Args:
                collection_name (str): The name of the collection to update.
                document_name (str): The name of the document whose points should be removed.
        """
        updated_results = self._client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_name",
                            match=models.MatchValue(value=document_name),
                        ),
                    ],
                )
            ),
        )


    def create_collection(self, collection_name: str, vector_field_dimension: int) -> bool:
        """
            Creates a new Qdrant collection with COSINE distance and indexes the 'document_name' payload field.
            Args:
                collection_name (str): The name for the new collection.
                vector_field_dimension (int): The dimensionality of the vectors in the collection.
            Returns:
                bool: True if the collection and payload index were successfully created.
            Raises:
                Exception: If collection creation or payload index creation fails.
        """
        success = self._client.create_collection(
            collection_name=collection_name,
            vectors_config= models.VectorParams(
                size=vector_field_dimension,
                distance=models.Distance.COSINE
            ),
        )
        if not success:
            raise Exception("Failed to create collection.")
        else:
            operation_result = self._client.create_payload_index(
                collection_name=collection_name,
                field_name="document_name",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
            if operation_result.status == "completed":
                print("Collection created successfully")
            else:
                # remove collection
                self._client.delete_collection(collection_name=collection_name)
                raise Exception("Failed to create collection. Error while creating payload index.")
        return success


    async def delete_collection(self, collection_name: str) -> bool:
        """
            Deletes an entire Qdrant collection.
            Args:
                collection_name (str): The name of the collection to delete.
            Returns:
                bool: True if the collection was successfully deleted.
            Raises:
                Exception: If collection deletion fails.
        """
        success = self._client.delete_collection(
            collection_name=collection_name
        )
        if not success:
            raise Exception("Failed to delete collection.")
        else:
            print("Collection deleted successfully.")
        return success


    async def list_unique_documents(self, collection_name: str) -> List[str]:
        """
            Retrieves a list of all unique document names present in the collection using facet search.
            Args:
                collection_name (str): The name of the collection to query.
            Returns:
                List[str]: A list of unique document names (strings).
        """
        results = self._client.facet(
            collection_name=collection_name,
            key="document_name"
        ).hits
        unique_documents = [hit.value for hit in results]
        return unique_documents

    def collection_exists(self, collection_name: str) -> bool:
        """
            Checks if a Qdrant collection with the given name already exists.
            Args:
                collection_name (str): The name of the collection to check.
            Returns:
                bool: True if the collection exists, False otherwise.
        """
        return self._client.collection_exists(collection_name=collection_name)
