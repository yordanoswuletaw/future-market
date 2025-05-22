import bytewax.operators as op
from bytewax.dataflow import Dataflow
from utils.config import settings
from core.db.qdrant import QdrantDatabaseConnector
from input_stream import RabbitMQSource
from output_stream import QdrantOutput
import pandas as pd 
from datetime import datetime, timezone
import pytz
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize the Qdrant database connector
connection = QdrantDatabaseConnector()

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Make sure not using GPU unless needed
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def clean_data(data):
    logger.info(f"Cleaning data: {data}")
    flattened_data = []
    for each in data:
        financial_markets_relevance_score = 0
        for topic in each['topics']:
            if topic['topic'] == 'Financial Markets':
                financial_markets_relevance_score = topic['relevance_score']
                break
        record = {
            "timestamp": each['time_published'],
            "title": each['title'],
            "summary": each['summary'],
            "overall_sentiment_score": each['overall_sentiment_score'],
            "overall_sentiment_label": each['overall_sentiment_label'],
            "financial_markets_relevance_score": financial_markets_relevance_score,
        }
    
        flattened_data.append(record)
    return pd.DataFrame(data=flattened_data)

# Function to get FinBERT sentiment for a given text
def get_finbert_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
    labels = ['bullish', 'neutral', 'bearish']
    sentiment_scores = {label: float(prob) for label, prob in zip(labels, probs[0])}
    predicted_label = labels[torch.argmax(probs)]
    return predicted_label, sentiment_scores

def convert_time_format(time: str) -> datetime:
    """Map time string to datetime object."""
    # Parse the input time
    parsed_time = datetime.strptime(time, '%Y%m%dT%H%M%S')

    # Convert to a specific time zone (e.g., US/Eastern)
    eastern = pytz.timezone("US/Eastern")
    local_time = pytz.utc.localize(parsed_time).astimezone(eastern)

    # Format the local time
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def compute_sentiment_scores(data):
    logger.info(f"Computing sentiment scores: {data}")
    news_articles = []
    for i in range(data.shape[0]):
        news_article = data.iloc[i]
        text = f"{news_article.get('timestamp', '')}. {news_article.get('summary', '')}. Financial Markets Relevance Score: {news_article.get('financial_markets_relevance_score', '')}. Overall Sentiment Score: {news_article.get('overall_sentiment_score', '')}. Overall Sentiment Label: {news_article.get('overall_sentiment_label', '')}"
        label, scores = get_finbert_sentiment(text)
        news_articles.append({
            "timestamp": convert_time_format(news_article.get("timestamp")),
            "actual_label": news_article.get("overall_sentiment_label"),
            "predicted_label": label,
            "bullish_sentiment_scores": scores.get('bullish', 0),
            "somewhat_bullish_sentiment_scores": scores.get('somewhat-bullish', 0),
            "neutral_sentiment_scores": scores.get('neutral', 0),
            "somewhat_bearish_sentiment_scores": scores.get('somewhat-bearish', 0),
            "bearish_sentiment_scores": scores.get('bearish', 0)
        })
    return pd.DataFrame(data=news_articles)

def create_news_sentiment_data_flow(flow: Dataflow):
    '''
    Create a data flow for news sentiment data
    '''
    # Listen to news data
    stream = op.input("news_input", flow, RabbitMQSource(settings.RABBITMQ_NEWS_QUEUE))

    logger.info(f"Stream: {stream}")

    stream = op.map("clean_news_data", stream, clean_data)
    stream = op.map("compute_sentiment_scores", stream, compute_sentiment_scores)
    
    # Add output operator
    op.output(
        "news_data_to_qdrant",
        stream,
        QdrantOutput(connection=connection, sink_type="clean"),
    )
    
    return stream
