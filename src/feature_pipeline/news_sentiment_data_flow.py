import bytewax.operators as op
from bytewax.dataflow import Dataflow
from utils.config import settings
from core.db.qdrant import QdrantDatabaseConnector
from input_stream import RabbitMQSource
from output_stream import QdrantOutput
# from data_logic.dispatchers import (
#     ChunkingDispatcher,
#     CleaningDispatcher,
#     EmbeddingDispatcher,
#     RawDispatcher,
# )

from utils.logger import get_logger

logger = get_logger(__name__)

connection = QdrantDatabaseConnector()

flow = Dataflow("News Sentiment Data Streaming Ingestion Pipeline")

def clean_data(data):
    logger.info(f"Cleaning data: {data}")
    return data

def create_news_sentiment_data_flow():
    '''
    Create a data flow for news sentiment data
    '''
    # Listen to news data
    stream = op.input("input", flow, RabbitMQSource(settings.RABBITMQ_NEWS_QUEUE))

    logger.info(f"Stream: {stream}")

    stream = op.map("clean dispatch", stream, clean_data)
    op.output(
        "cleaned data insert to qdrant",
        stream,
        QdrantOutput(connection=connection, sink_type="vector"),
    )

    return flow
