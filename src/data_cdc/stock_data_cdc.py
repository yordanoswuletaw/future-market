import json
from bson import json_util

from core.db.mongo import connection
from core.mq import publish_to_rabbitmq
from utils.config import settings
from utils.logger import get_logger

logger = get_logger(__file__)

_database = connection.get_database('future_market')
# Create a collection
_collection = _database[settings.STOCK_COLLECTION_NAME]

def stream_stock_data_process():
    try:
        # Watch changes in a specific collection
        changes = _collection.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])

        for change in changes:
            print('STOCK DATA CHANGE: ', change)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    stream_stock_data_process()
