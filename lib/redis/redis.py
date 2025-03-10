from redis import Redis

from lib.config.config import REDIS_PORT, REDIS_SERVER

redis_client: Redis = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=0)
