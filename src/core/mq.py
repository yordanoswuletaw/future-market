from typing import Self

import pika
import json

from utils.config import settings
from utils.logger import get_logger

from core.db.mongo import connection

logger = get_logger(__file__)


class RabbitMQConnection:
    """Singleton class to manage RabbitMQ connection."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        virtual_host: str = "/",
        fail_silently: bool = False,
        **kwargs,
    ) -> None:
        self.host = host or settings.RABBITMQ_HOST
        self.port = port or settings.RABBITMQ_PORT
        self.username = username or settings.RABBITMQ_DEFAULT_USERNAME
        self.password = password or settings.RABBITMQ_DEFAULT_PASSWORD
        self.virtual_host = virtual_host
        self.fail_silently = fail_silently
        self._connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                    credentials=credentials,
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            logger.exception("Failed to connect to RabbitMQ:")
            if not self.fail_silently:
                raise e

    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_open

    def get_channel(self):
        if self.is_connected():
            return self._connection.channel()

    def close(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None
            print("Closed RabbitMQ connection")



# Get a database instance
_database = connection.get_database('future_market')
# Create an instance of RabbitMQConnection
_rabbitmq_conn = RabbitMQConnection()

def publish_to_rabbitmq(collection_name: str, queue_name: str):
    """Listen to data changes and Publish data to a RabbitMQ queue."""
    try:
        # Get a collection
        _collection = _database[collection_name]

        # Establish connection
        with _rabbitmq_conn:
            channel = _rabbitmq_conn.get_channel()

            # Ensure the queue exists
            channel.queue_declare(queue=queue_name, durable=True)

            # Delivery confirmation
            channel.confirm_delivery()
            
            # Change Stream Listener
            with _collection.watch() as stream:
                for change in stream:   

                    # Serialize change event
                    message = str(change)

                    # Send data to the queue
                    channel.basic_publish(
                        exchange="",
                        routing_key=queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                        ),
                    )
                    logger.info(f"Published message to queue: {queue_name}")
                    
    except pika.exceptions.UnroutableError:
        logger.warning("Message could not be routed")
    except Exception:
        logger.exception("Error publishing to RabbitMQ.")


if __name__ == "__main__":
    publish_to_rabbitmq("test_queue", "Hello, World!")
