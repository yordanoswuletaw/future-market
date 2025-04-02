from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Batch, Distance, VectorParams

from utils.logger import get_logger
from utils.config import settings

logger = get_logger(__name__)


class QdrantDatabaseConnector:
    _instance: QdrantClient | None = None

    def __init__(self):
        '''
        Initialize the QdrantClient singleton instance
        '''
        if self._instance is None:
            if settings.USE_QDRANT_CLOUD:
                self._instance = QdrantClient(
                    url=settings.QDRANT_CLOUD_URL,
                    api_key=settings.QDRANT_APIKEY,
                )
            else:
                self._instance = QdrantClient(
                    url=settings.QDRANT_DATABASE_HOST,
                    port=settings.QDRANT_DATABASE_PORT,
                )
    
    def create_vector_collection(self, collection_name: str = settings.VECTOR_COLLECTION_NAME) -> None:
        '''
        Create a vector collection in Qdrant
        '''
        try:
            self._instance.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_SIZE, 
                    distance=Distance.COSINE
                ),
            )
        except Exception as e:
            logger.error(f"Error creating vector collection: {e}")
    
    def create_non_vector_collection(self, collection_name: str = settings.NON_VECTOR_COLLECTION_NAME) -> None:
        '''
        Create a non-vector collection in Qdrant
        '''
        try:
            self._instance.create_collection(collection_name=collection_name, vectors_config={})
        except Exception as e:
            logger.error(f"Error creating non-vector collection: {e}")
    
    def get_collection(self, collection_name: str):
        '''
        Get a collection from Qdrant
        '''
        return self._instance.get_collection(collection_name=collection_name)

    def write_data(self, collection_name: str, points: Batch) -> None:
        '''
        Write data to a collection in Qdrant
        '''
        try:        
            self._instance.add(
                collection_name=collection_name,
                points=points)
        except Exception as e:
            logger.error(f"Error writing data to collection: {e}")
            raise e
    
    def search(
            self, 
            collection_name: str, 
            query_vector: list, 
            query_filter: models.Filter, 
            limit: int = 3) -> list[models.PointStruct]:
        '''
        Search data in a collection in Qdrant
        '''
        return self._instance.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit
        )
    
    def scroll(self, collection_name: str, limit: int = 3) -> list[models.PointStruct]:
        '''
        Scroll through data in a collection in Qdrant
        '''
        return self._instance.scroll(
            collection_name=collection_name,
            limit=limit
        )

    def close(self) -> None:
        '''
        Close the QdrantClient connection
        '''
        if self._instance:
            self._instance.close()
            logger.info("Qdrant DB connection closed")
        else:
            logger.warning("Qdrant DB connection not initialized")
