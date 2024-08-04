from .base_site import BaseSite
from ..requester import Requester
from ..logger import logger
import math
from ..helpers import fetch_pages, remove_duplicates_in_list
import urllib.error

class Geonode(BaseSite):
    url = "https://geonode.com"
    request_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page={}&sort_by=lastChecked&sort_type=desc"
    PROXIES_PER_PAGE = 100

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        logger.debug(f"Starting proxy extraction from {self.url}")
        total_pages = self._get_total_pages()
        all_pages = self._get_all_pages(total_pages)

        proxies = []
        for page in all_pages:
            for proxy_info in page.get("data", []):
                proxy = self._parse_proxy(proxy_info)
                if proxy:
                    proxies.append(proxy)

        unique_proxies = remove_duplicates_in_list(proxies)
        logger.debug(f"Extracted {len(unique_proxies)} unique proxies from {self.url}")
        return unique_proxies

    def _get_total_pages(self):
        try:
            response = self.requester.make_request(self.request_url.format(1), as_json=True)
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP Error fetching total pages from {self.url}: {e}")
            return 0
        
        total_pages = math.ceil(response["total"] / self.PROXIES_PER_PAGE)
        logger.debug(f"Total pages to fetch from {self.url}: {total_pages}")
        return total_pages
    
    def _get_all_pages(self, total_pages):
        logger.debug(f"Fetching {total_pages} pages from {self.url}")
        return fetch_pages(
            url=self.request_url, 
            total_pages=total_pages
        )
    
    def _parse_proxy(self, proxy_info):
        ip = proxy_info.get("ip", "")
        port = proxy_info.get("port", "")

        # TODO: Should get implemented
        # username = proxy_info.get("username")
        # password = proxy_info.get("password")

        # if username and password:
        #     return f"{username}:{password}@{ip}:{port}"

        if not ip or not port:
            logger.warning(f"Invalid proxy info: {proxy_info} in {self.url}")
            return None
        
        logger.debug(f"Parsed proxy: {ip}:{port}")
        return f"{ip}:{port}"