from .base_site import BaseSite
from proxin.requester import Requester
from proxin.helpers import fetch_pages, remove_duplicates_in_list, keep_only_digits
from proxin.logger import logger
import math

class IPRoyal(BaseSite):
    url = "https://iproyal.com"
    request_url = f"{url}/free-proxy-list/?page={{}}&entries=100"
    PROXIES_PER_PAGE = 100

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        try:
            total_pages = self._get_total_pages()
            if total_pages == 0:
                return []

            all_pages = fetch_pages(
                url=self.request_url,
                total_pages=total_pages,
                parse_as_json=False,
                parse_as_soup=True,
            )
            proxies = self._parse_all_proxies(all_pages)
            return remove_duplicates_in_list(proxies)
        except Exception as e:
            logger.error(f"Error extracting proxies: {e}")
            return []

    def _get_total_pages(self):
        try:
            soup = self.requester.make_request(
                self.request_url.format(1), 
                as_soup=True
            )
            if not soup:
                return 0

            number_span = soup.find('span', class_='text-onInfoOutline')
            if not number_span:
                logger.warning("Could not find the total number of proxies span")
                return 0

            total_proxies = int(keep_only_digits(number_span.text.strip()) or 0)
            return math.ceil(total_proxies / self.PROXIES_PER_PAGE)
        
        except Exception as e:
            logger.error(f"Error getting total pages: {e}")
            return 0

    def _parse_all_proxies(self, pages):
        all_proxies = []
        for page in pages:
            proxies = self._parse_proxy_page(page)
            all_proxies.extend(proxies)
        return all_proxies

    def _parse_proxy_page(self, page):
        try:
            proxy_divs = page.find_all('div', style="grid-template-columns: repeat(5, 1fr)")
            return [self._parse_proxy_div(div) for div in proxy_divs if div]
        except Exception as e:
            logger.error(f"Error parsing proxy page: {e}")
            return []

    def _parse_proxy_div(self, div):
        try:
            ip = div.find_all('div')[0].text.strip()
            port = div.find_all('div')[1].text.strip()
            
            if not keep_only_digits(ip) or not keep_only_digits(port):
                return None

            return f"{ip}:{port}"
        except Exception as e:
            logger.error(f"Error parsing proxy div: {e}")
            return None