from typing import Optional
import requests

from pydantic import UUID4, BaseModel, ConfigDict, Field

from utils.logger import get_logger

from core.db.mongo import connection
from utils.config import settings

_database = connection.get_database('future_market')
# Create a collection
_collection = _database[settings.STOCK_COLLECTION_NAME]
# Unique index to prevent duplicate stock data
_collection.create_index([("symbol", 1), ("timestamp", 1)], unique=True)
# TTL index to automatically delete data older than 1 years
_collection.create_index("ttl", expireAfterSeconds=31536000)

logger = get_logger(__name__)

class StockData(BaseModel):

    @classmethod
    def _fetch_live_data(cls) -> Optional[dict]:
        """Fetch live data from Alpha Vantage API."""
        response = requests.get(settings.URL)
        if response.status_code == 200:
            data = response.json()
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            symbol = data['Meta Data']['2. Symbol']

            return {'symbol': symbol, 'last_refreshed': last_refreshed, 'data': data.get(f"Time Series ({settings.INTERVAL})", {})}  # Adjust key based on API response
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
        symbol = data['symbol']

        try:
            for timestamp, record in data['data'].items():
                stock_entry = {
                    "symbol": symbol,
                    "timestamp": timestamp,
                    "batch": last_refreshed,
                    "open": float(record["1. open"]),
                    "high": float(record["2. high"]),
                    "low": float(record["3. low"]),
                    "close": float(record["4. close"]),
                    "volume": int(record["5. volume"])
                }
                _collection.insert_one(stock_entry)

            logger.info("Data inserted successfully.")

        except:
            logger.exception("Failed to update or create document.")
            return None

StockData.insert_or_update()