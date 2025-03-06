from abc import abstractmethod

from bs4 import BeautifulSoup, Tag
from lib.sources.BaseSource import BaseSource
from requests import Response, get


class BaseScrapingSource(BaseSource):
    def _get_html(self, url) -> BeautifulSoup:

        res: Response = get(url)

        if res.status_code != 200:
            res.raise_for_status()

        return BeautifulSoup(res.text, "html.parser")

    @abstractmethod
    def _get_news_tags(self, source_html) -> list[Tag]:
        pass

    @abstractmethod
    def _get_full_story(self, tag: Tag) -> dict:
        pass

    @abstractmethod
    def _extract_news_details(self, source_html) -> list[Tag]:
        pass

    @abstractmethod
    def _get_title(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def _get_link(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def _get_timestamp(self, tag: Tag) -> int:
        pass

    def _get_image_url(self, tag: Tag) -> str:
        pass

    def _get_text(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def _get_story_category(self, story: str) -> str:
        pass
