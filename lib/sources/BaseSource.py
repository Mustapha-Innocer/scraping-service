from abc import ABC, abstractmethod

from lib.logging.logger import LOGGER


class BaseSource(ABC):
    def __init__(self):
        LOGGER.info(f"Initializing {self.name} source")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    async def push_data(self, waitime: int):
        pass
