import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_PORT = os.getenv("KAFKA_PORT")

REDIS_SERVER = os.getenv("REDIS_SERVER")
REDIS_PORT = os.getenv("REDIS_PORT")
