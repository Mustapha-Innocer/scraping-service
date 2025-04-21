from abc import ABC, abstractmethod

from lib.logging.logger import LOGGER


class BaseSource(ABC):
    def __init__(self, wait_time: int):
        self.wait_time = wait_time if wait_time and wait_time > 0 else 3600
        LOGGER.info(f"Initializing {self.name} source.")
        LOGGER.info(f"Waiting time is {self.wait_time}")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    async def push_data(self):
        pass
