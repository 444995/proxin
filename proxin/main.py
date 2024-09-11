import sys
import importlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from proxin.helpers import get_domain, remove_duplicates_in_list
from proxin.sites.base_site import BaseSite
from proxin.sites.generic import Generic as GenericExtractor
from proxin.processor import process_proxies
from proxin.logger import logger
from proxin.outputter import Outputter
import argparse

def load_site_class(domain):
    site_path = os.path.join(os.path.dirname(__file__), 'sites')
    for file in os.listdir(site_path):
        if file.endswith('.py') and file != 'base_site.py' and not file.startswith('unfinished__'):
            module = importlib.import_module(f"proxin.sites.{file[:-3]}")
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseSite) and attr_value is not BaseSite:
                    if hasattr(attr_value, 'url') and attr_value.url == domain:
                        return attr_value
    return GenericExtractor

def process_url(url):
    domain = get_domain(url)
    site_class = load_site_class(domain)
    return process_proxies(site_class, url)

def main():
    parser = argparse.ArgumentParser(description="proxin - Python tool for extracting proxies from various online sources")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', nargs='+', help='URL(s) to process (comma-separated for multiple)')
    group.add_argument('--file', help='File containing URLs to process (one per line)')
    parser.add_argument('--keep-duplicates', action='store_true', help='Keep duplicate proxies (default: remove duplicates)')
    args = parser.parse_args()

    urls = []
    if args.url:
        urls = [url.strip() for url in ','.join(args.url).split(',')]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"File not found: {args.file}")
            sys.exit(1)

    if not urls:
        logger.error("No URLs provided")
        sys.exit(1)

    all_proxies = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                proxies = future.result()
                all_proxies.extend(proxies)
                logger.info(f"Processed {url} - found {len(proxies)} proxies")
            except Exception as exc:
                logger.error(f"{url} generated an exception: {exc}")

    if not args.keep_duplicates:
        all_proxies = remove_duplicates_in_list(all_proxies)
        logger.info(f"Removed duplicates. Total unique proxies: {len(all_proxies)}")
    else:
        logger.info(f"Kept all proxies including duplicates. Total proxies: {len(all_proxies)}")

    outputter = Outputter(output_folder="results")
    output_file = outputter.output_result(all_proxies)
    logger.info(f"All proxies saved to: {output_file}")

if __name__ == "__main__":
    main()