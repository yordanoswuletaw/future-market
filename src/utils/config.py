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
    LIMIT: int = 3
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


    # LLMS Configs
    GEMINI_MODEL_NAME: str = 'gemini-1.0-pro-001'


    class Config:
        env_file = f"{ROOT_DIR}/.env"
        env_file_encoding = "utf-8"


settings = AppSettings()