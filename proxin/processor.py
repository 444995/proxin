from proxin.logger import logger
from proxin.outputter import Outputter

def process_proxies(site_class, url):
    try:
        logger.info(f"Initializing {site_class.__name__} for URL: {url}")
        site_instance = site_class()
        if hasattr(site_instance, 'set_url'):
            site_instance.set_url(url)
        
        logger.info("Extracting proxies...")
        proxies = site_instance.extract_proxies()
        
        logger.info(f"Found {len(proxies)} proxies")
        logger.debug(f"Extracted proxies: {proxies}")
        
        outputter = Outputter(output_folder="results")
        output_file = outputter.output_result(proxies)
        
        logger.info(f"Proxies saved to {output_file}")
        return proxies
    except Exception as e:
        logger.error(f"Error processing proxies: {e}")
        return []