from .base_site import BaseSite
from proxin.requester import Requester
from proxin.logger import logger
from proxin.helpers import remove_duplicates_in_list, clean_proxy_string
from urllib.parse import urlparse, urljoin

class ProxyScrape(BaseSite):
    url = "https://proxyscrape.com"
    request_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text"

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        logger.debug(f"Starting proxy extraction from ProxyScrape")
        content = self.requester.make_request(self.request_url, as_json=False)
        if not content:
            return []
        proxies = self._parse_proxies(content)
        logger.debug(f"Extracted {len(proxies)} proxies from ProxyScrape")
        return remove_duplicates_in_list(proxies)

    def _parse_proxies(self, content):
        return [clean_proxy_string(proxy) for proxy in content.split("\n")]