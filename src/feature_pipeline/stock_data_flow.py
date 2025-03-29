import bytewax.operators as op
from bytewax.dataflow import Dataflow
from utils.config import settings
from core.db.qdrant import QdrantDatabaseConnector
from feature_pipeline.input_stream import RabbitMQSource
# from data_flow.stream_output import QdrantOutput
# from data_logic.dispatchers import (
#     ChunkingDispatcher,
#     CleaningDispatcher,
#     EmbeddingDispatcher,
#     RawDispatcher,
# )

from utils.logger import get_logger

logger = get_logger(__name__)

connection = QdrantDatabaseConnector()

flow = Dataflow("Stock Data Streaming Ingestion Pipeline")

def clean_data(data):
    logger.info(f"Cleaning data: {data}")
    return data


def create_stock_data_flow():
    '''
    Create a data flow for stock data
    '''
    # Listen to stock data
    stream = op.input("input", flow, RabbitMQSource(settings.RABBITMQ_STOCK_QUEUE))

    logger.info(f"Stream: {stream}")

    stream = op.map("clean dispatch", stream, clean_data)
    # op.output(
    #     "cleaned data insert to qdrant",
    #     stream,
    #     QdrantOutput(connection=connection, sink_type="clean"),
    # )
    # stream = op.flat_map("chunk dispatch", stream, ChunkingDispatcher.dispatch_chunker)
    # stream = op.map(
    #     "embedded chunk dispatch", stream, EmbeddingDispatcher.dispatch_embedder
    # )
    # op.output(
    #     "embedded data insert to qdrant",
    #     stream,
    #     QdrantOutput(connection=connection, sink_type="vector"),
    # )