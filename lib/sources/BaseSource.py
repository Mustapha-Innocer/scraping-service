from abc import ABC, abstractmethod

from lib.sources.typings import SourceArticle


class BaseSource(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def base_url(self):
        pass

    def top_headlines(self) -> list[SourceArticle]:
        pass
