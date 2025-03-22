from datetime import datetime
from lib.logging.logger import LOGGER

from bs4 import BeautifulSoup, Tag

from lib.sources.ScrapingSources.BaseScrapingSource import BaseScrapingSource
from lib.decorators.decorator import check_cache


class CityNews(BaseScrapingSource):
    def __init__(self):
        self.__name = "city news gh"
        self.__url = "https://citinewsroom.com/news/"
        super().__init__()

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @check_cache
    def _get_news_tags(self, source_html: BeautifulSoup) -> set[Tag]:
        LOGGER.debug("Extracting news tags")
        news_tags: list[Tag] = source_html.find_all(
            "h3", class_="jeg_post_title"
        )
        return set(news_tags)

    def _get_title(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story title")
        title: str = story_html.find("h1", class_="jeg_post_title").text
        return title

    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        LOGGER.info("Extracting story timestamp")
        date_str: str = (
            story_html.find("div", class_="meta_left")
            .find("div", class_="jeg_meta_date")
            .find("a")
            .text
        )
        date = datetime.strptime(date_str, "%B %d, %Y")
        return int(date.timestamp())

    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story image url")
        img_url: str = story_html.find(
            "div", class_="jeg_featured featured_image"
        ).find("img")["src"]
        return img_url

    def _get_text(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story body")
        text: str = story_html.find("div", class_="content-inner").text
        return text

    def _get_author(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story author")
        tag: Tag = story_html.select_one(
            "div.meta_left > div.jeg_meta_author.coauthor"
        )
        if tag and tag.find("a"):
            return tag.find("a").text
        LOGGER.info("Author name not found")
        return "unknown"
