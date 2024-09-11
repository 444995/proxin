import time
from proxin.requester import Requester
from urllib.parse import urlparse
from proxin.logger import logger
import re

def keep_only_digits(text):
    try:
        return int(''.join(filter(str.isdigit, text)))
    except ValueError:
        logger.debug(f"Could not extract digits from text: {text}")
        return None
    
def clean_proxy_string(proxy_string):
    return re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', proxy_string).group(0) \
            if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', proxy_string) else ""

def get_domain(url):
    """
    Extracts the domain from a URL.
    """
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def remove_duplicates_in_list(input_list):
    """
    Removes duplicates and *empty lines* from the list and returns a new list.
    """
    return list(set(item.strip() for item in input_list if item.strip()))

def fetch_pages(url, total_pages, parse_as_json=True, parse_as_soup=False, max_retries=5, exp_backoff_retry_delay=60):
    # TODO: Should probably have a normal delay and then the exp backoff is optional - set by True/False
    """
    Fetches data from a site with paginated results.

    Parameters:
    url (str): The URL template for the site with a placeholder for the page number.
    total_pages (int): The total number of pages to fetch.
    parse_as_json (bool): Whether to parse the response as JSON. Default is True.
    max_retries (int): The maximum number of retries allowed for each page request. Default is 5.
    exp_backoff_retry_delay (int): The initial delay in seconds before retrying after a failure. Default is 60 seconds.

    Returns:
    list: A list containing the aggregated data from all pages.

    The function iterates over the specified number of pages and attempts to fetch data from each page.
    If a request fails, it retries up to 'max_retries' times with an exponential backoff delay.
    The delay between retries starts at 'exp_backoff_retry_delay' seconds and doubles after each failed attempt.
    If the maximum number of retries is reached and the request still fails, an error message is logged and the function
    proceeds to the next page.
    """
    requester = Requester()

    all_data = []
    
    for page_num in range(1, total_pages + 1):
        logger.debug(f"Fetching page {page_num} of {total_pages}...")
        page_url = url.format(page_num)
        
        attempt = 0
        while attempt <= max_retries:
            try:
                page_data = requester.make_request(page_url, as_json=parse_as_json, as_soup=parse_as_soup)
                if page_data:
                    all_data.append(page_data)
                    logger.debug(f"Successfully fetched data from page {page_num}")
                break  # Exit the retry loop if the request is successful
            except Exception as e:
                attempt += 1
                if attempt > max_retries:
                    logger.error(f"Failed to fetch page {page_num} after {max_retries} retries. Error: {e}")
                    break
                backoff_time = exp_backoff_retry_delay * (2 ** (attempt - 1))
                logger.warning(f"Attempt {attempt} failed because of {e}. Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
    
    logger.debug(f"Fetched a total of {len(all_data)} pages")
    return all_data