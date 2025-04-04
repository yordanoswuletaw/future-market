import bytewax.operators as op
from bytewax.dataflow import Dataflow
from stock_data_flow import create_stock_data_flow
from news_sentiment_data_flow import create_news_sentiment_data_flow
from utils.logger import get_logger

logger = get_logger(__name__)

def build_flow():
    """Create and return a combined Bytewax dataflow."""
    # Create a new dataflow
    flow = Dataflow("Combined Streaming Ingestion Data Pipeline")
    
    # Create stock data stream
    stock_stream = create_stock_data_flow(flow)
    # Create news sentiment stream
    news_stream = create_news_sentiment_data_flow(flow)
    
    # Combine both streams
    combined = op.merge("combine_streams", stock_stream, news_stream)
    
    return flow

if __name__ == "__main__":
    build_flow()