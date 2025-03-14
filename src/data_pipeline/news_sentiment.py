from typing import Optional
import requests

from datetime import datetime
import pytz

from pydantic import UUID4, BaseModel, ConfigDict, Field

from utils.logger import get_logger

from core.db.mongo import connection
from utils.config import settings

_database = connection.get_database("future_market")

logger = get_logger(__name__)

class NewsSentiment(BaseModel):

    @classmethod
    def _convert_time_format(cls, time: str) -> datetime:
        """Map time string to datetime object."""
        # Parse the input time
        parsed_time = datetime.strptime(time, '%Y%m%dT%H%M%S')

        # Convert to a specific time zone (e.g., US/Eastern)
        eastern = pytz.timezone("US/Eastern")
        local_time = pytz.utc.localize(parsed_time).astimezone(eastern)

        # Format the local time
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _fetch_live_news(cls) -> Optional[dict]:
        """Fetch live data from Alpha Vantage API."""
        response = requests.get(settings.NEWS_URL)
        if response.status_code == 200:
            data = response.json()
            return list(map(lambda news: {
                "title": news['title'],
                "summary": news['summary'],
                "timestamp": cls._convert_time_format(news['time_published']),
                "overall_sentiment_score": news["overall_sentiment_score"],
                "overall_sentiment_label": news["overall_sentiment_label"],
                "content": news["url"],
                "topics": news['topics'],
                "ticker_sentiment": news["ticker_sentiment"]
            }, data['feed']))

        else:
            get_logger(f"Error fetching data: {response.status_code}")
            return None
    
    @classmethod
    def insert_or_update(cls) -> None:
        """Update MongoDB with new data."""
        data = cls._fetch_live_news()
        if not data:
            logger.error("No data fetched from API.")
        
        print(data[:3])
        
    #     last_refreshed = data['last_refreshed']
    #     data = data['data']

    #     try:
    #         collection = _database[cls._get_collection_name()]
    #         for timestamp, record in data.items():
    #             stock_entry = {
    #                 "timestamp": timestamp,
    #                 "batch": last_refreshed,
    #                 "open": float(record["1. open"]),
    #                 "high": float(record["2. high"]),
    #                 "low": float(record["3. low"]),
    #                 "close": float(record["4. close"]),
    #                 "volume": int(record["5. volume"])
    #             }
    #             collection.insert_one(stock_entry)

    #         logger.info("Data inserted successfully.")

    #     except:
    #         logger.exception("Failed to update or create document.")
    #         return None
    
    @classmethod
    def _get_collection_name(cls) -> str:
        return 'news_sentiment'

NewsSentiment.insert_or_update()