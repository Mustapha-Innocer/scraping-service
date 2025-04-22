from datetime import datetime

from bs4 import BeautifulSoup, Tag

from lib.decorators.decorator import check_cache
from lib.exceptions.NotFound import Notfound
from lib.logging.logger import LOGGER
from lib.sources.ScrapingSources.BaseScrapingSource import BaseScrapingSource


class CityNews(BaseScrapingSource):
    def __init__(self, wait_time: int | None = None):
        self.__name = "City News"
        self.__url = "https://citinewsroom.com/news/"
        self.__country = "Ghana"
        self.__country_code = "GH"
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
                "h3", class_="jeg_post_title"
            )
            return set(news_tags)
        except Exception as e:
            raise Notfound(f"Unable to find news tags: {str(e)}")

    def _get_title(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story title")
        try:
            title: str = story_html.find("h1", class_="jeg_post_title").text
            return title
        except Exception as e:
            raise Notfound(f"Unable to extract story title: {str(e)}")

    def _get_timestamp(self, story_html: BeautifulSoup) -> int:
        LOGGER.info("Extracting story timestamp")
        try:
            date_str: str = (
                story_html.find("div", class_="meta_left")
                .find("div", class_="jeg_meta_date")
                .find("a")
                .text
            )
            date = datetime.strptime(date_str, "%B %d, %Y")
            return int(date.timestamp())
        except Exception as e:
            raise Notfound(f"Unable to extract story timestamp: {str(e)}")

    def _get_image_url(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story image url")
        try:
            img_url: str = story_html.find(
                "div", class_="jeg_featured featured_image"
            ).find("img")["src"]
            return img_url
        except Exception as e:
            raise Notfound(f"Unable to extract story image url: {str(e)}")

    def _get_text(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story body")
        try:
            text: str = story_html.find("div", class_="content-inner").text
            return text
        except Exception as e:
            raise Notfound(f"Unable to extract story content: {str(e)}")

    def _get_author(self, story_html: BeautifulSoup) -> str:
        LOGGER.info("Extracting story author")
        try:
            tag: Tag = story_html.select_one(
                "div.meta_left > div.jeg_meta_author.coauthor"
            )
            if tag and tag.find("a"):
                return tag.find("a").text
            LOGGER.info("Author name not found")
            return "unknown"
        except Exception as e:
            raise Notfound(f"Unable to extract story author: {str(e)}")
