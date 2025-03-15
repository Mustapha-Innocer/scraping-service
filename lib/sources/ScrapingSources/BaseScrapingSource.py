import json
from abc import abstractmethod
from asyncio import gather, sleep

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from lib.kafka.producer import delivery_report, kafka_producer
from lib.logging.logger import LOGGER
from lib.sources.BaseSource import BaseSource
from lib.sources.typings import ScrapedData


class BaseScrapingSource(BaseSource):
    def __init__(self):
        super().__init__()

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
            async with session.get(url) as res:
                if res.status != 200:
                    LOGGER.error(f"Unaccessible URL: {url}")
                    return
                text = await res.text()
        return BeautifulSoup(text, "html.parser")

    async def _process(self, tag: Tag, session: ClientSession) -> None:
        url = tag.a["href"]
        LOGGER.debug(f"Getting full story HTML from {url}")
        async with session.get(url) as response:
            if response.status != 200:
                LOGGER.error(f"Failed to get story HTML from {url}")
                return

            text = await response.text()
            story_html = BeautifulSoup(text, "html.parser")
            LOGGER.info(f"Processing {tag.a.text}")
            title = self._get_title(story_html)
            timestamp = self._get_timestamp(story_html)
            image_url = self._get_image_url(story_html)
            text = self._get_text(story_html)
            author = self._get_author(story_html)

            data = ScrapedData(
                url=url,
                title=title,
                body=text,
                timestamp=timestamp,
                image_url=image_url,
                source=self.name,
                author=author,
            )

            with kafka_producer() as producer:
                producer.produce(
                    topic="news-data",
                    value=json.dumps(data.__dict__),
                    callback=delivery_report,
                )

    async def push_data(self, waitime: int = 3600):
        while True:
            LOGGER.info(f"Scraping data from {self.name}")
            LOGGER.debug(f"Geeting stories HTML from {self.url}")
            source_html: BeautifulSoup = await self._get_html(self.url)
            news_tags = self._get_news_tags(source_html)
            LOGGER.info(f"Found {len(news_tags)} news stories")
            async with ClientSession() as session:
                await gather(
                    *[self._process(tag, session) for tag in news_tags]
                )
            await sleep(waitime)
