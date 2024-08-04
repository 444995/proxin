from .base_site import BaseSite
import base64
from ..requester import Requester
from ..logger import logger
from bs4 import BeautifulSoup

class FreeProxyCz(BaseSite):
    # TODO: Should extract proxies from all pages, not just main page
    url = "http://free-proxy.cz"
    request_url = "http://free-proxy.cz/en/"

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
            site_data = self.requester.make_request(self.request_url, as_json=False)
            logger.debug(f"Successfully fetched site data from {self.url}")
            return site_data
        except Exception as e:
            logger.error(f"Error fetching site data from {self.url}: {e}")
        return None

    def _parse_proxies(self, soup):
        proxies = []
        rows = soup.find_all('tr')
        logger.debug(f"Found {len(rows)} rows to parse")
        for row in rows:
            try:
                proxy = self._extract_proxy_from_row(row)
                if proxy:
                    proxies.append(proxy)
            except Exception as e:
                logger.warning(f"Error parsing row: {e}")
        logger.debug(f"Successfully parsed {len(proxies)} proxies")
        return proxies

    def _extract_proxy_from_row(self, row):
        ip_script = row.find('script')
        port_span = row.find('span', class_='fport')

        if ip_script and port_span:
            ip = self._decode_ip(ip_script.string.strip())
            port = port_span.string.strip()
            if ip and port:
                proxy = f"{ip}:{port}"
                logger.debug(f"Extracted proxy: {proxy}")
                return proxy
        logger.debug("Row does not contain valid proxy information")
        return None

    def _decode_ip(self, encoded_ip_string):
        try:
            encoded_ip = encoded_ip_string.split('"')[1]
            decoded_ip = base64.b64decode(encoded_ip).decode('utf-8')
            logger.debug(f"Successfully decoded IP: {decoded_ip}")
            return decoded_ip
        except (IndexError, base64.binascii.Error) as e:
            logger.error(f"Error decoding IP: {e}")
        return None