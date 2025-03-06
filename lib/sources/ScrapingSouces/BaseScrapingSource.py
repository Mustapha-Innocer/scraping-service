from abc import abstractmethod

from bs4 import BeautifulSoup, Tag
from lib.sources.BaseSource import BaseSource
from lib.sources.typings import ScrapedData
from requests import Response, get


class BaseScrapingSource(BaseSource):
    def _get_html(self, url) -> BeautifulSoup:

        res: Response = get(url)

        if res.status_code != 200:
            res.raise_for_status()

        return BeautifulSoup(res.text, "html.parser")

    @abstractmethod
    def _get_news_tags(self, source_html) -> set[Tag]:
        pass

    @abstractmethod
    def _extract_data(self, source_html) -> ScrapedData:
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
