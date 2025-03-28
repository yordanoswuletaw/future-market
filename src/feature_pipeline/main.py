import bytewax.operators as op
from bytewax.dataflow import Dataflow
from utils.config import settings
from core.db.qdrant import QdrantDatabaseConnector
from input_stream import RabbitMQSource
# from data_flow.stream_output import QdrantOutput
# from data_logic.dispatchers import (
#     ChunkingDispatcher,
#     CleaningDispatcher,
#     EmbeddingDispatcher,
#     RawDispatcher,
# )

connection = QdrantDatabaseConnector()

flow = Dataflow("Streaming ingestion pipeline")
# Listen to stock data
stream = op.input("input", flow, RabbitMQSource(settings.RABBITMQ_STOCK_QUEUE))

# # Listen to news data
# stream = op.input("input", flow, RabbitMQSource(settings.RABBITMQ_NEWS_QUEUE))

# stream = op.map("raw dispatch", stream, RawDispatcher.handle_mq_message)
# stream = op.map("clean dispatch", stream, CleaningDispatcher.dispatch_cleaner)
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
