from proxin.logger import logger

def process_proxies(site_class, url):
    try:
        site_instance = site_class()

        if hasattr(site_instance, 'custom_url') and site_instance.custom_url:
            proxies = site_instance.extract_proxies(url)
        else:
            proxies = site_instance.extract_proxies()
        
        return proxies
    except Exception as e:
        logger.error(f"Error processing proxies: {e}")
        return []