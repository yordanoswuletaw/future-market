from data_pipeline.stock_data import StockData
from data_pipeline.news_sentiment import NewsSentiment
from core.mq import publish_to_rabbitmq
from utils.config import settings

from time import sleep

def main():

    # Fetch stock data
    StockData.insert_or_update()

    # Fetch news sentiment
    NewsSentiment.insert_or_update()

    # Listen to stock data changes and publish to a RabbitMQ queue
    publish_to_rabbitmq(settings.STOCK_COLLECTION_NAME, settings.RABBITMQ_STOCK_QUEUE)

    # Listen to news sentiment changes and publish to a RabbitMQ queue
    publish_to_rabbitmq(settings.NEWS_COLLECTION_NAME, settings.RABBITMQ_NEWS_QUEUE) 

if __name__ == "__main__":
    main()
