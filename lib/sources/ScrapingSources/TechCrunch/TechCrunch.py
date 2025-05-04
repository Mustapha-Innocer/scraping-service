from datetime import datetime

from bs4 import BeautifulSoup, Tag

from lib.decorators.decorator import check_cache
from lib.exceptions.NotFound import Notfound
from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.BaseScrapingSource import BaseScrapingSource


class TechCrunch(BaseScrapingSource):
    def __init__(self, wait_time: int | None = None):
        self.__name = "Tech Crunch"
        self.__url = "https://techcrunch.com/latest/"
        self.__country = "United States"
        self.__country_code = "US"
        super().__init__(wait_time)

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def country(self):
        return self.__country

    @property
    def country_code(self):
        return self.__country_code

    @check_cache
    def _get_news_tags(self, source_html: BeautifulSoup) -> set[Tag]:
        LOGGER.debug("Extracting news tags")
        try:
            news_tags: list[Tag] = source_html.find_all(
                "h3", class_="loop-card__title"
            )
            return set(news_tags)
        except Exception as e:
            raise Notfound(f"Unable to find news tags: {str(e)}")

    def _get_title(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story title")
        try:
            title: str = story_html.find(
                "h1", class_="article-hero__title wp-block-post-title"
            ).text
            return title
        except Exception as e:
            raise Notfound(f"Unable to extract story title: {str(e)}")

    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        LOGGER.info("Extracting story timestamp")
        try:
            date_str: str = story_html.find(
                "div", class_="article-hero__date"
            ).find("time")["datetime"]
            date = datetime.fromisoformat(date_str)
            return int(date.timestamp())
        except Exception as e:
            raise Notfound(f"Unable to extract story timestamp: {str(e)}")

    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story image url")
        try:
            img_url: str = story_html.find(
                "div", class_="article-hero__first-section"
            ).find("img")["src"]
            return img_url
        except Exception as e:
            raise Notfound(f"Unable to extract story image url: {str(e)}")

    def _get_text(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story body")
        try:
            text: str = story_html.find(
                "div",
                class_="wp-block-post-content-is-layout-constrained",
            ).text
            return text
        except Exception as e:
            raise Notfound(f"Unable to extract story content: {str(e)}")

    def _get_author(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story author")
        try:
            tag: Tag = story_html.select_one("div.article-hero__authors")
            return tag.find("a").text
        except Exception as e:
            raise Notfound(f"Unable to extract story author: {str(e)}")
