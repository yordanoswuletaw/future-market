import bytewax.operators as op
from bytewax.dataflow import Dataflow
from utils.config import settings
from core.db.qdrant import QdrantDatabaseConnector
from input_stream import RabbitMQSource
from output_stream import QdrantOutput
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from functools import partial

from utils.logger import get_logger

logger = get_logger(__name__)

connection = QdrantDatabaseConnector()

def clean_and_structure_data(data) -> pd.DataFrame:
    logger.info(f"Cleaning data: {data}")
    return pd.DataFrame(data=data).set_index('timestamp').sort_index(inplace=True)

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    # Price Based Features
    df["price_change"] = df["close"].diff()               # Δclose
    df["return"] = df["close"].pct_change()  # % return
    df['log_return'] = np.log(df['close']).diff()             # log return
    df["high_low_range"] = df["high"] - df["low"]         # volatility proxy
    df["close_open_diff"] = df["close"] - df["open"]
    df['avg_price'] = df[['open', 'high', 'low', 'close']].mean(axis=1)

    # Lag Features
    df['lag1_close'] = df['close'].shift(1)
    df['lag1_return'] = df['return'].shift(1)
    df['lag2_return'] = df['return'].shift(2)

    # Calculate moving averages for 5, 10, and 15 periods
    df['ma_5'] = df['close'].rolling(window=5).mean()
    df['ma_10'] = df['close'].rolling(window=10).mean()
    df['ema_5'] = df['close'].ewm(span=5, adjust=False).mean()

    # Volume moving average (5 periods) and change
    df['vol_ma_5'] = df['volume'].rolling(window=5).mean()
    df['vol_change'] = df['volume'].diff()

    # Time Features
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    
    return df

def create_multiclass_target(df, threshold=0.0005):  # 0.05% threshold
    df = df.copy()
    def classify_return(ret):
        if ret > threshold:
            return "bullish"
        elif ret < -threshold:
            return "bearish"
        else:
            return "neutral"

    df["target"] = df["close"].pct_change().shift(-1).apply(classify_return)
    return df

def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    # Encode time features
    le = LabelEncoder()
    df['hour'] = le.fit_transform(df['hour'])
    df['minute'] = le.fit_transform(df['minute'])
    df['target'] = le.fit_transform(df['target'])
    
    return df

def create_stock_data_flow(flow: Dataflow):
    '''
    Create a data flow for stock data
    '''
    # Listen to stock data
    stream = op.input("stock_input", flow, RabbitMQSource(settings.RABBITMQ_STOCK_QUEUE))

    logger.info(f"Stream: {stream}")

    stream = op.map("clean_stock_data", stream, clean_and_structure_data)
    stream = op.map("compute_features", stream, compute_features)
    stream = op.map("create_multiclass_target", stream, partial(create_multiclass_target, threshold=0.0005))
    stream = op.map("encode_features", stream, encode_features)
    
    # Add output operator
    op.output(
        "stock_data_to_qdrant",
        stream,
        QdrantOutput(connection=connection, sink_type="clean"),
    )
    
    return stream