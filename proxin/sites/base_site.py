from abc import ABC, abstractmethod

class BaseSite(ABC):
    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def extract_proxies(self):
        pass