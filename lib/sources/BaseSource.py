from abc import ABC, abstractmethod

from lib.sources.typings import ScrapedData


class BaseSource(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def top_headlines(self) -> list[ScrapedData]:
        pass
