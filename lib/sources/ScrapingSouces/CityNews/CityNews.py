import logging
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from lib.sources.ScrapingSouces.BaseScrapingSource import BaseScrapingSource
from lib.sources.typings import ScrapedData

LOGGER = logging.getLogger(__name__)


class CityNews(BaseScrapingSource):
    def __init__(self):
        self.__name = "city news gh"
        self.__base_url = "https://citinewsroom.com"

    @property
    def name(self):
        return self.__name

    @property
    def base_url(self):
        return self.__base_url

    def _get_news_tags(self, source_html: BeautifulSoup) -> set[Tag]:
        news_tags: list[Tag] = source_html.find_all(
            "h3", class_="jeg_post_title"
        )

        # TODO: handle empty news_tags

        return set(news_tags)

    def _extract_data(self, tag: Tag) -> ScrapedData:
        url = tag.a["href"]

        story_html = self._get_html(url)

        # TODO: handle empty story_html

        title = self._get_title(story_html)
        timestamp = self._get_timestamp(story_html)
        image_url = self._get_image_url(story_html)
        text = self._get_text(story_html)
        author = self._get_author(story_html)

        source_article = ScrapedData(
            url=url,
            title=title,
            body=text,
            timestamp=timestamp,
            image_url=image_url,
            source=self.__name,
            author=author,
        )

        return source_article

    def _get_title(self, story_html: BeautifulSoup) -> str:
        title: str = story_html.find("h1", class_="jeg_post_title").text
        return title

    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        date_str: str = (
            story_html.find("div", class_="meta_left")
            .find("div", class_="jeg_meta_date")
            .find("a")
            .text
        )
        date = datetime.strptime(date_str, "%B %d, %Y")
        return int(date.timestamp())

    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        img_url: str = story_html.find(
            "div", class_="jeg_featured featured_image"
        ).find("img")["src"]
        return img_url

    def _get_text(self, story_html: BeautifulSoup) -> str:
        text: str = story_html.find("div", class_="content-inner").text
        return text

    def _get_author(self, story_html: BeautifulSoup) -> str:
        tag: Tag = story_html.select_one(
            "div.meta_left > div.jeg_meta_author.coauthor"
        )
        if tag and tag.find("a"):
            return tag.find("a").text
        return "unknown"

    def top_headlines(self) -> list[ScrapedData]:
        res = []
        url: str = f"{self.__base_url}/news/"
        source_html: BeautifulSoup = self._get_html(url)
        news_tags = self._get_news_tags(source_html)
        LOGGER.info(f"Found {len(news_tags)} headlines")
        for tag in news_tags:
            data: ScrapedData = self._extract_data(tag)
            # TODO: publish data to a message broker
            res.append(data)
        return res
