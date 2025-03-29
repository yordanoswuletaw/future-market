from stock_data_flow import create_stock_data_flow
from news_sentiment_data_flow import create_news_sentiment_data_flow

def build_flow():
    """Create and return multiple Bytewax dataflows."""
    stock_data_flow = create_stock_data_flow()  # Stock Data Flow
    sentiment_data_flow = create_news_sentiment_data_flow()  # Sentiment Analysis Flow
    return [stock_data_flow, sentiment_data_flow]