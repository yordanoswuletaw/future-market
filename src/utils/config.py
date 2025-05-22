from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = str(Path(__file__).parent.parent.parent)

class AppSettings(BaseSettings):

    # Alpha Vantage API Settings
    ALPHA_VANTAGE_API_KEY: str 
    FUNCTION: str = "TIME_SERIES_INTRADAY"  # Example: Fetch intraday data
    SYMBOL: str = "IBM"  # Stock symbol -> AAPL | MSFT | GOOGL | AMZN | TSLA | IBM | ORCL | INTC | CSCO | FB
    INTERVAL: str = "5min"  # Data interval -> 1min | 5min | 15min | 30min | 60min
    OUTPUT_SIZE: str = "full"  # Output size -> compact | full
    DATA_TYPE: str = "json"  # Data type -> json | csv
    # for news sentiment
    NEWS_FUNCTION: str = "NEWS_SENTIMENT"
    LIMIT: int = 100
    TICKERS: str = 'IBM'
    # TIME_FROM: str = "20220410T0130"
    # TIME_TO: str = "20220410T0130"
    @property
    def URL(self) -> str:
        return f"https://www.alphavantage.co/query?function={self.FUNCTION}&symbol={self.SYMBOL}&interval={self.INTERVAL}&outputsize={self.OUTPUT_SIZE}&apikey={self.ALPHA_VANTAGE_API_KEY}&datatype={self.DATA_TYPE}"
    
    @property
    def NEWS_URL(self) -> str:
        return f"https://www.alphavantage.co/query?function={self.NEWS_FUNCTION}&tickers={self.TICKERS}&apikey={self.ALPHA_VANTAGE_API_KEY}&limit={self.LIMIT}"



    # MongoDB Configs
    MONGO_DATABASE_HOST: str = (
        "mongodb://mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=future-market-replica-set"
    )
    MONGO_DATABASE_NAME: str = "future_market"
    STOCK_COLLECTION_NAME: str = "stock_data"
    NEWS_COLLECTION_NAME: str = "news_sentiment"


    # MQ config
    RABBITMQ_DEFAULT_USERNAME: str = "guest"
    RABBITMQ_DEFAULT_PASSWORD: str = "guest"
    # RABBITMQ_HOST: str = "mq"
    # RABBITMQ_PORT: int = 5672
    RABBITMQ_HOST: str = "mq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_STOCK_QUEUE: str = "stock_data"
    RABBITMQ_NEWS_QUEUE: str = "news_sentiment"

    # QdrantDB config
    QDRANT_DATABASE_HOST: str = "qdrant"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: str = "str"
    QDRANT_APIKEY: str 
    USE_QDRANT_CLOUD: bool = False

    # Embedding Configs
    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 512
    EMBEDDING_SIZE: int = 384
    EMBEDDING_MODEL_DEVICE: str = "cpu"
    VECTOR_COLLECTION_NAME: str = "news_sentiment"
    NON_VECTOR_COLLECTION_NAME: str = "stock_data"


    class Config:
        env_file = f"{ROOT_DIR}/.env"
        env_file_encoding = "utf-8"


settings = AppSettings()