from .base_method import BaseMethod
import re
from ..helpers import remove_duplicates_in_list

class RegexProxyExtractor(BaseMethod):
    def __init__(self, site_data):
        super().__init__(site_data)
        self.proxy_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b')

    def extract_proxies(self):
        if not self.site_data:
            return []
        
        proxies = self.proxy_pattern.findall(self.site_data)
        
        return remove_duplicates_in_list(proxies)