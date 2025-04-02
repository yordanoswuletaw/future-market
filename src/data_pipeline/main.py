from news_sentiment import NewsSentiment
from stock_data import StockData

if __name__ == "__main__":
    NewsSentiment.insert_or_update()
    StockData.insert_or_update()