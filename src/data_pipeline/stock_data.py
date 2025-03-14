from typing import Optional
import requests

from pydantic import UUID4, BaseModel, ConfigDict, Field

from utils.logger import get_logger

from core.db.mongo import connection
from utils.config import settings

_database = connection.get_database("future_market")

logger = get_logger(__name__)

class StockData(BaseModel):

    @classmethod
    def _fetch_live_data(cls) -> Optional[dict]:
        """Fetch live data from Alpha Vantage API."""
        response = requests.get(settings.URL)
        if response.status_code == 200:
            data = response.json()
            last_refreshed = data['Meta Data']['3. Last Refreshed']

            return {'last_refreshed': last_refreshed, 'data': data.get(f"Time Series ({settings.INTERVAL})", {})}  # Adjust key based on API response
        else:
            get_logger(f"Error fetching data: {response.status_code}")
            return None
    
    @classmethod
    def insert_or_update(cls) -> None:
        """Update MongoDB with new data."""
        data = cls._fetch_live_data()
        if not data or data['data'] == {}:
            logger.error("No data fetched from API.")
        
        last_refreshed = data['last_refreshed']
        data = data['data']

        try:
            collection = _database[cls._get_collection_name()]
            for timestamp, record in data.items():
                stock_entry = {
                    "timestamp": timestamp,
                    "batch": last_refreshed,
                    "open": float(record["1. open"]),
                    "high": float(record["2. high"]),
                    "low": float(record["3. low"]),
                    "close": float(record["4. close"]),
                    "volume": int(record["5. volume"])
                }
                collection.insert_one(stock_entry)

            logger.info("Data inserted successfully.")

        except:
            logger.exception("Failed to update or create document.")
            return None
    
    @classmethod
    def _get_collection_name(cls) -> str:
        return 'stock_data'

StockData.insert_or_update()