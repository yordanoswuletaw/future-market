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

def clean_data(data):
    logger.info(f"Cleaning data: {data}")
    return data

def create_stock_data_flow(flow: Dataflow):
    '''
    Create a data flow for stock data
    '''
    # Listen to stock data
    stream = op.input("stock_input", flow, RabbitMQSource(settings.RABBITMQ_STOCK_QUEUE))

    logger.info(f"Stream: {stream}")

    stream = op.map("clean_stock_data", stream, clean_data)
    
    # Add output operator
    op.output(
        "stock_data_to_qdrant",
        stream,
        QdrantOutput(connection=connection, sink_type="clean"),
    )
    
    return stream