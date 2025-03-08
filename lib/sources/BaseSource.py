from abc import ABC, abstractmethod


class BaseSource(ABC):
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
