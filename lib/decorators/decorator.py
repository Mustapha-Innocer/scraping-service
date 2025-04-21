import json

from lib.config.config import TTL_NEW_TAG
from lib.logging.logger import LOGGER
from lib.redis.redis import redis_client
from lib.util.util import hash_string


def check_cache(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        new_res = []
        for data in res:
            url = data.a["href"]
            try:
                if redis_client.get(hash_string(url)):
                    LOGGER.info(f"Already processed, Skipping {url}")
                    continue
                new_res.append(data)
            except Exception as e:
                LOGGER.error(f"Unable to read from Cache: {str(e)}")
        return new_res

    return wrapper


def add_to_cache(func):
    def wrapper(*args, **kwargs):
        LOGGER.info("Adding new item to the cache")
        err = args[0]
        if err:
            return func(*args, **kwargs)
        message = json.loads(args[1].value())
        url = message["url"]
        try:
            redis_client.setex(hash_string(url), TTL_NEW_TAG, message["title"])
        except Exception as e:
            LOGGER.error(f"Unable to cache {url} \n{str(e)}")
        return func(*args, **kwargs)

    return wrapper
