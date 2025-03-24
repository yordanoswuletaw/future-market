from utils.logger import get_logger

from core.db.mongo import connection
from utils.config import settings

logger = get_logger(__name__)

_database = connection.get_database('future_market')

def data_change_streams(collection_name: str, queue_name):
    """Listen to stock data changes."""
    # Get a collection
    _collection = _database[collection_name]
    
    # Change Stream Listener
    with _collection.watch() as stream:
        for change in stream:
            print(change)