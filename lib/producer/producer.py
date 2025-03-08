import json
from contextlib import contextmanager

from confluent_kafka import Producer
from config import config

# Kafka configuration
config = {
    "bootstrap.servers": config.KAFKA_SERVER,
    "client.id": "scraping-service",
    "acks": "1",
    "retries": 2,
    "compression.codec": "gzip",
}


# Callback function for delivery report
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        # TODO: add to cache
        message = json.loads(msg.value())
        print(f"Message delivered to {msg.topic()} - {message['title']}")


@contextmanager
def kafka_producer():
    producer = Producer(config)
    try:
        yield producer
    finally:
        producer.flush()
