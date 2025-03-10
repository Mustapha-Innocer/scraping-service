import json
from contextlib import contextmanager

from confluent_kafka import Producer

from lib.config.config import KAFKA_PORT, KAFKA_SERVER
from lib.decorators.decorator import add_to_cache
from lib.logging.logger import LOGGER
from lib.redis.redis import redis_client
from lib.util.util import hash_string

# Kafka configuration
config = {
    "bootstrap.servers": f"{KAFKA_SERVER}:{KAFKA_PORT}",
    "client.id": "scraping-service",
    "acks": "1",
    "retries": 2,
    "compression.codec": "gzip",
}


# Callback function for delivery report
@add_to_cache
def delivery_report(err, msg):
    if err:
        LOGGER.info(f"Data delivery failed: {err}")
    else:
        message = json.loads(msg.value())
        redis_client.setex(hash_string(message["url"]), 600, message["title"])
        LOGGER.info(f"Data delivered to {msg.topic()} - {message['title']}")


@contextmanager
def kafka_producer():
    producer = Producer(config)
    try:
        yield producer
    finally:
        producer.flush()
