from .base_site import BaseSite
from proxin.requester import Requester
from proxin.logger import logger
from proxin.helpers import remove_duplicates_in_list
from urllib.parse import urlparse, urljoin

class Github(BaseSite):
    url = "https://github.com"
    custom_url = True

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self, url):
        logger.debug(f"Starting proxy extraction from GitHub: {url}")
        raw_content_url = self._get_raw_content_url(url)

        if not raw_content_url:
            return []

        content = self.requester.make_request(raw_content_url, as_json=False)
        if not content:
            return []

        proxies = self._parse_proxies(content)
        logger.debug(f"Extracted {len(proxies)} proxies from GitHub")
        return remove_duplicates_in_list(proxies)

    def _get_raw_content_url(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        if len(path_parts) < 5 or path_parts[3] != "blob":
            logger.error("Invalid GitHub URL format")
            return None
        raw_path = '/'.join(path_parts[:3] + path_parts[4:])
        return urljoin("https://raw.githubusercontent.com", raw_path)

    def _parse_proxies(self, content):
        return [proxy.strip() for proxy in content.split("\n")]