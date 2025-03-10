import functools

from lib.logging.logger import LOGGER
from lib.redis.redis import redis_client
from lib.util.util import hash_string


def check_cache(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        for data in res.copy():
            url = data.a["href"]
            if redis_client.get(hash_string(url)):
                LOGGER.info(f"Already processed, Skipping {url}")
                res.remove(data)
        return res

    return wrapper


def add_to_cache(func):
    def wrapper(*args, **kwargs):
        LOGGER.info("Cache updated")
        return func(*args, **kwargs)

    return wrapper
