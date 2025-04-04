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
            data_type = change["ns"]["coll"]
            change["fullDocument"].pop("_id")

            if data_type != settings.STOCK_COLLECTION_NAME:
                logger.info(f"Unsupported data type: '{data_type}'")
                continue

            # Use json_util to serialize the document
            data = json.dumps(change["fullDocument"], default=json_util.default)
            logger.info(
                f"Change detected and serialized for a data sample of type {data_type}."
            )

            # Send data to rabbitmq
            publish_to_rabbitmq(queue_name=settings.RABBITMQ_STOCK_QUEUE, data=data)
            logger.info(f"Data of type '{data_type}' published to RabbitMQ.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     stream_stock_data_process()
