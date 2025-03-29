import threading

from data_pipeline.stock_data import StockData
from data_pipeline.news_sentiment import NewsSentiment
from core.mq import publish_to_rabbitmq
from utils.config import settings

from time import sleep

def start_mq_publishing(collection_name, queue_name):
    '''
    Start a thread to publish data to RabbitMQ
    '''
    print('-----STARTING MQ PUBLISHING-----')
    thread = threading.Thread(target=publish_to_rabbitmq, args=(collection_name, queue_name), daemon=True)
    thread.start()

def start_fetching_data(target_function):
    '''
    Start the Bytewax pipeline
    '''
    print('-----STARTING BYTEWAX PIPELINE-----')
    thread = threading.Thread(target=target_function, daemon=True)
    thread.start()

def main():
    '''
    Main function to run the data pipeline
    '''

    # Start publishing to RabbitMQ
    start_mq_publishing(settings.STOCK_COLLECTION_NAME, settings.RABBITMQ_STOCK_QUEUE)
    start_mq_publishing(settings.NEWS_COLLECTION_NAME, settings.RABBITMQ_NEWS_QUEUE)

    # Fetch stock data
    start_fetching_data(StockData.insert_or_update)
    # Fetch news sentiment
    start_fetching_data(NewsSentiment.insert_or_update)
    
    while True:
        sleep(10)

if __name__ == "__main__":
    main()
