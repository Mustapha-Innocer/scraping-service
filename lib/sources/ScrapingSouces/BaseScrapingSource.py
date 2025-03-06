from abc import abstractmethod

from bs4 import BeautifulSoup, Tag
from lib.sources.BaseSource import BaseSource
from requests import Response, get


class BaseScrapingSource(BaseSource):
    def __get(url) -> BeautifulSoup:

        res: Response = get(url)

        if res.status_code != 200:
            res.raise_for_status()

        return BeautifulSoup(res.text, "html.parser")

    @abstractmethod
    def __get_news_tags(self, source_html) -> list[Tag]:
        pass

    @abstractmethod
    def __get_full_story(self, tag: Tag) -> dict:
        pass

    @abstractmethod
    def __extract_news_details(self, source_html) -> list[Tag]:
        pass

    @abstractmethod
    def __get_title(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def __get_link(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def __get_timestamp(self, tag: Tag) -> int:
        pass

    def __get_image_url(self, tag: Tag) -> str:
        pass

    def __get_text(self, tag: Tag) -> str:
        pass

    @abstractmethod
    def __get_story_category(self, story: str) -> str:
        pass
