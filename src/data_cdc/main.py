from concurrent.futures import ThreadPoolExecutor

from stock_data_cdc import stream_stock_data_process
from news_sentiment_cdc import stream_news_sentiment_process

def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(stream_stock_data_process)
        executor.submit(stream_news_sentiment_process)

    executor.shutdown(wait=True)

if __name__ == "__main__":
    main()