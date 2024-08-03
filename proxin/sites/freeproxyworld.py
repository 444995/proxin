from .base_site import BaseSite
from ..requester import Requester
from bs4 import BeautifulSoup

class FreeProxyWorld(BaseSite):
    url = "https://www.freeproxy.world"
    #request_url = "https://www.freeproxy.world/"
    request_url = "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page={}"

    PROXIES_PER_PAGE = 50

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        try:
            site_data = self._get_site_data()
            if site_data:
                soup = BeautifulSoup(site_data, "html.parser")
                return self._parse_proxies(soup)
        except Exception as e:
            print(f"Error extracting proxies: {e}")
        return []

    def _get_site_data(self):
        try:
            site_data = self.requester.make_request(self.request_url, as_json=False)
            return site_data
        except Exception as e:
            print(f"Error fetching site data: {e}")
        return None

    def _parse_proxies(self, soup):
        total_pages = self._extract_total_pages(soup)
        
        proxies = []
        rows = soup.select('table.layui-table tbody tr')

        for row in rows:
            try:
                proxy = self._extract_proxy_from_row(row)
                if proxy:
                    proxies.append(proxy)
            except Exception as e:
                print(f"Error parsing row: {e}")
        return proxies
    
    def _extract_total_pages(self, soup):
        proxy_table_pages_div = soup.find('div', class_='proxy_table_pages')['data-counts']
        total_proxies = proxy_table_pages_div['data-counts']

        return int(total_proxies) // self.PROXIES_PER_PAGE

    def _extract_proxy_from_row(self, row):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].get_text(strip=True)
            port = cols[1].get_text(strip=True)
            return f"{ip}:{port}"
        return None
