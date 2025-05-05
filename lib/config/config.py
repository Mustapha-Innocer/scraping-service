import os

from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
KAFKA_PRODUCER_TOPIC = os.getenv("KAFKA_PRODUCER_TOPIC", "news-data")

REDIS_SERVER = os.getenv("REDIS_SERVER", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

TTL_NEW_TAG: int = int(os.getenv("TTL_NEW_TAG", 864000))
TTL_ERRORED_TAG: int = int(os.getenv("TTL_ERRORED_TAG", 432000))
