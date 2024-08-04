from .base_site import BaseSite
from ..requester import Requester
from ..logger import logger
from bs4 import BeautifulSoup

class FreeProxyWorld(BaseSite):
    url = "https://www.freeproxy.world"
    request_url = "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page={}"
    PROXIES_PER_PAGE = 50

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        logger.debug(f"Starting proxy extraction from {self.url}")
        try:
            site_data = self._get_site_data()
            if site_data:
                soup = BeautifulSoup(site_data, "html.parser")
                proxies = self._parse_proxies(soup)
                logger.debug(f"Extracted {len(proxies)} proxies from {self.url}")
                return proxies
        except Exception as e:
            logger.error(f"Error extracting proxies from {self.url}: {e}")
        return []

    def _get_site_data(self):
        try:
            site_data = self.requester.make_request(self.request_url.format(1), as_json=False)
            logger.debug(f"Successfully fetched site data from {self.url}")
            return site_data
        except Exception as e:
            logger.error(f"Error fetching site data from {self.url}: {e}")
        return None

    def _parse_proxies(self, soup):
        total_pages = self._extract_total_pages(soup)
        logger.debug(f"Total pages to parse: {total_pages}")
        
        proxies = []
        rows = soup.select('table.layui-table tbody tr')

        for row in rows:
            try:
                proxy = self._extract_proxy_from_row(row)
                if proxy:
                    proxies.append(proxy)
            except Exception as e:
                logger.warning(f"Error parsing row: {e}")
        return proxies
    
    def _extract_total_pages(self, soup):
        try:
            proxy_table_pages_div = soup.find('div', class_='proxy_table_pages')
            total_proxies = int(proxy_table_pages_div['data-counts'])
            total_pages = total_proxies // self.PROXIES_PER_PAGE
            logger.debug(f"Extracted total pages: {total_pages}")
            return total_pages
        except Exception as e:
            logger.error(f"Error extracting total pages: {e}")
            return 1  # Default to 1 page if extraction fails

    def _extract_proxy_from_row(self, row):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].get_text(strip=True)
            port = cols[1].get_text(strip=True)
            proxy = f"{ip}:{port}"
            logger.debug(f"Extracted proxy: {proxy}")
            return proxy
        logger.warning("Invalid row structure, couldn't extract proxy")
        return None