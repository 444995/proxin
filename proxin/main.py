import sys
import importlib
import os
from proxin.helpers import get_domain
from proxin.sites.base_site import BaseSite
from proxin.sites.generic import Generic as GenericExtractor
from proxin.processor import process_proxies
from proxin.logger import logger

def load_site_class(domain):
    logger.info(f"Loading site class for domain: {domain}")
    site_path = os.path.join(os.path.dirname(__file__), 'sites')
    for file in os.listdir(site_path):
        if file.endswith('.py') and file != 'base_site.py' and not file.startswith('unfinished__'):
            module = importlib.import_module(f"proxin.sites.{file[:-3]}")
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseSite) and attr_value is not BaseSite:
                    if hasattr(attr_value, 'url') and attr_value.url == domain:
                        logger.info(f"Found matching site class: {attr_value.__name__}")
                        return attr_value
    logger.info("No specific site class found, using GenericExtractor")
    return GenericExtractor

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--url':
        logger.error("Invalid command. Usage: proxin --url <url>")
        print("Usage: proxin --url <url>")
        sys.exit(1)

    url = sys.argv[2]
    logger.info(f"Starting proxy extraction for URL: {url}")
    domain = get_domain(url)
    site_class = load_site_class(domain)
    process_proxies(site_class, url)

if __name__ == "__main__":
    main()