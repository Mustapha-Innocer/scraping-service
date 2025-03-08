import json
from abc import abstractmethod
from asyncio import gather, sleep

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from requests import Response, get

from lib.producer.producer import delivery_report, kafka_producer
from lib.sources.BaseSource import BaseSource
from lib.sources.typings import ScrapedData


class BaseScrapingSource(BaseSource):
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

    def _get_html(self, url: str) -> BeautifulSoup:

        res: Response = get(url)

        if res.status_code != 200:
            res.raise_for_status()

        return BeautifulSoup(res.text, "html.parser")

    async def _process(self, tag: Tag, session) -> ScrapedData:
        url = tag.a["href"]
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()

            text = await response.text()
            story_html = BeautifulSoup(text, "html.parser")

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
            source_html: BeautifulSoup = self._get_html(self.url)
            news_tags = self._get_news_tags(source_html)
            async with ClientSession() as session:
                await gather(
                    *[self._process(tag, session) for tag in news_tags]
                )
            await sleep(waitime)
