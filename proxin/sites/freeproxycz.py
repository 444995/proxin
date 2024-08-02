from .base_site import BaseSite
import base64
from ..requester import Requester
from bs4 import BeautifulSoup

class FreeProxyCz(BaseSite):
    # TODO: Should extract proxies from all pages, not just main page
    url = "http://free-proxy.cz"
    request_url = "http://free-proxy.cz/en/"

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
        proxies = []
        rows = soup.find_all('tr')
        for row in rows:
            try:
                proxy = self._extract_proxy_from_row(row)
                if proxy:
                    proxies.append(proxy)
            except Exception as e:
                print(f"Error parsing row: {e}")
        return proxies

    def _extract_proxy_from_row(self, row):
        ip_script = row.find('script')
        port_span = row.find('span', class_='fport')

        if ip_script and port_span:
            ip = self._decode_ip(ip_script.string.strip())
            port = port_span.string.strip()
            return f"{ip}:{port}"
        return None

    def _decode_ip(self, encoded_ip_string):
        try:
            encoded_ip = encoded_ip_string.split('"')[1]
            return base64.b64decode(encoded_ip).decode('utf-8')
        except (IndexError, base64.binascii.Error) as e:
            print(f"Error decoding IP: {e}")
        return None
