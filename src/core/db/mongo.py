from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__file__)


class MongoDatabaseConnector:
    """Singleton class to connect to MongoDB database."""

    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
                logger.info(
                    f"Connection to database with uri: {settings.MONGO_DATABASE_HOST} successful"
                )
            except ConnectionFailure:
                logger.error(f"Couldn't connect to the database.")

                raise

        return cls._instance

    def get_collection(self, name: str, expire_time: int = 31536000):
        assert self._instance, "Database connection not initialized"
     
        _database = self._instance[settings.MONGO_DATABASE_NAME]
        
        # Get the collection
        _collection = _database[name]

        # Unique index to prevent duplicate stock data
        _collection.create_index([("symbol", 1), ("timestamp", 1)], unique=True)

        # TTL index to automatically delete data older than 1 years
        _collection.create_index("data_age", expireAfterSeconds=expire_time)
        return _collection
    

    def close(self):
        if self._instance:
            self._instance.close()
            logger.info("Connected to database has been closed.")


connection = MongoDatabaseConnector()
