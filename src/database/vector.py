from abc import ABC, abstractmethod
from qdrant_client import QdrantClient, models
from ..data_models import DataPoint
from typing import List
import uuid
from loguru import Logger


logger = Logger()


class VectorDatabase(ABC):
    @abstractmethod
    def insert(self, points: List[DataPoint]) -> bool:
        pass

    @abstractmethod
    def retrieve(self, queries) -> List[DataPoint]:
        pass

    @abstractmethod
    def remove(self, ids: List[uuid.UUID]):
        pass


class QdrantVectorDatabase(ABC):
    def __init__(self, url: str, port: int, https: bool | None = None):
        self._client = QdrantClient(
            url=url,
            port=port,
            https=https,
        )

    def _create_qdrant_points(self, data_points: List[DataPoint]) -> List[models.PointStruct]:
        qdrant_points = []
        for p in data_points:
            qdrant_points.append(
                models.PointStruct(
                    id=uuid.uuid4().hex,
                    vector={

                    },
                    payload={

                    }
                )
            )
        return qdrant_points

    def insert(self, data_points: List[DataPoint], collection_name: str, batch_size: int = 10_000) -> bool:
        qdrant_points = self._create_qdrant_points(data_points)
        try:
            self._client.upload_points(
                collection_name=collection_name,
                points=qdrant_points,
                batch_size=batch_size,
                wait=True
            )
        except Exception as e:
            logger.error(f"Error occurred while inserting points into qdrant collection {collection_name}. Exception: {str(e)}")
            return False
        logger.info(f"Successfully uploaded points to Qdrant collection {collection_name}")
        return True


    @abstractmethod
    def retrieve(self, queries) -> List[DataPoint]:
        pass

    @abstractmethod
    def remove(self, ids: List[uuid.UUID]):
        pass