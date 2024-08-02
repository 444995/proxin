from abc import ABC, abstractmethod

class BaseMethod(ABC):
    def __init__(self, site_data):
        self.site_data = site_data

    @abstractmethod
    def extract_proxies(self):
        pass
