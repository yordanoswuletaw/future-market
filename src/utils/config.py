from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = str(Path(__file__).parent.parent.parent)

class AppSettings(BaseSettings):

    # Alpha Vantage API Settings
    ALPHA_VANTAGE_API_KEY: str | None
    FUNCTION: str = "TIME_SERIES_INTRADAY"  # Example: Fetch intraday data
    SYMBOL: str = "AAPL"  # Stock symbol -> AAPL | MSFT | GOOGL | AMZN | TSLA | IBM | ORCL | INTC | CSCO | FB
    INTERVAL: str = "5min"  # Data interval -> 1min | 5min | 15min | 30min | 60min
    OUTPUT_SIZE: str = "full"  # Output size -> compact | full
    DATA_TYPE: str = "csv"  # Data type -> json | csv
    URL: str = f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&interval={INTERVAL}&outputsize={OUTPUT_SIZE}&apikey={ALPHA_VANTAGE_API_KEY}&datatype={DATA_TYPE}"
    
    class Config:
        env_file = f'{ROOT_DIR}/.env'

settings = AppSettings()