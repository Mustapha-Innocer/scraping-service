import json
from abc import abstractmethod
from asyncio import gather, sleep
import traceback

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from lib.config.config import TTL_ERRORED_TAG, KAFKA_PRODUCER_TOPIC
from lib.kafka.producer import delivery_report, kafka_producer
from lib.logging.logger import LOGGER
from lib.redis.redis import redis_client
from lib.sources.BaseSource import BaseSource
from lib.util.util import hash_string


class BaseScrapingSource(BaseSource):
    def __init__(self, wait_time):
        super().__init__(wait_time)

    @property
    @abstractmethod
    def country(self):
        pass

    @property
    @abstractmethod
    def country_code(self):
        pass

    @abstractmethod
    def _get_news_tags(self, source_html: BeautifulSoup) -> set[Tag]:
        pass

    @abstractmethod
    def _get_title(self, story_html: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        pass

    @abstractmethod
    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_text(self, story_html: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_author(self, story_html: BeautifulSoup) -> str:
        pass

    async def _get_html(self, url: str) -> BeautifulSoup:

        async with ClientSession() as session:
            headers = {"user-agent": "Mozilla/5.0 ..."}
            async with session.get(url, headers=headers) as res:
                if res.status != 200:
                    LOGGER.error(f"Unaccessible URL: {url}")
                    return
                text = await res.text()
        return BeautifulSoup(text, "html.parser")

    async def _process(self, tag: Tag) -> None:
        url = tag.a["href"]
        try:
            LOGGER.debug(f"Getting full story HTML from {url}")
            story_html = await self._get_html(url)
            LOGGER.info(f"Processing {tag.a.text}")
            title = self._get_title(story_html)
            timestamp = self._get_timestamp(story_html)
            image_url = self._get_image_url(story_html)
            text = self._get_text(story_html)
            author = self._get_author(story_html)

            data = {
                "url": url,
                "title": title,
                "body": text,
                "published_at": timestamp,
                "image_url": image_url,
                "source": {
                    "name": self.name,
                    "country": self.country,
                    "country_code": self.country_code,
                },
                "author": author,
            }

            with kafka_producer() as producer:
                producer.produce(
                    topic=KAFKA_PRODUCER_TOPIC,
                    value=json.dumps(data),
                    callback=delivery_report,
                )
        except Exception as e:
            LOGGER.error(f"Unable to process {str(e)}")
            traceback.print_exc()
            try:
                redis_client.setex(
                    hash_string(url), TTL_ERRORED_TAG, tag.a.text
                )
            except Exception as e:
                LOGGER.error(f"Unable to cache {url} \n{str(e)}")

    async def push_data(self):
        while True:
            LOGGER.info(f"Scraping data from {self.name}")
            LOGGER.debug(f"Geting stories HTML from {self.url}")
            source_html: BeautifulSoup = await self._get_html(self.url)
            if source_html is not None:
                news_tags = self._get_news_tags(source_html)
                LOGGER.info(f"Found {len(news_tags)} news stories")
                await gather(*[self._process(tag) for tag in news_tags])
            await sleep(self.wait_time)
