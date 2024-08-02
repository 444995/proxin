import os
import sys
import importlib
from urllib.parse import urlparse
from .sites.base_site import BaseSite
from .methods.base_method import BaseMethod
from .requester import Requester

def get_domain(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def find_site_class(domain):
    site_path = os.path.join(os.path.dirname(__file__), 'sites')
    for file in os.listdir(site_path):
        if file.endswith('.py') and file != 'base.py':
            module_name = f"proxin.sites.{file[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseSite) and attr_value is not BaseSite:
                    if attr_value.url == domain:
                        return attr_value
    return None

def try_methods(site_data):
    methods_path = os.path.join(os.path.dirname(__file__), 'methods')
    methods = []
    for file in os.listdir(methods_path):
        if file.endswith('.py') and file != 'base.py':
            module_name = f"proxin.methods.{file[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseMethod) and attr_value is not BaseMethod:
                    methods.append(attr_value(site_data))
    proxies = []
    for method in methods:
        try:
            proxies.extend(method.extract_proxies())
        except Exception as e:
            print(f"Method {method.__class__.__name__} failed: {e}")
    return proxies

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--url':
        print("Usage: proxin --url <url>")
        sys.exit(1)
    
    url = sys.argv[2]
    domain = get_domain(url)
    
    site_class = find_site_class(domain)
    if site_class:
        site_instance = site_class()
        proxies = site_instance.extract_proxies()
    else:
        requester = Requester()
        site_data = requester.make_request(url, as_json=False)
        proxies = try_methods(site_data)
    
    print(f"Found {len(proxies)} proxies")
    for proxy in proxies:
        print(proxy)
        input('Press Enter to get next proxy')

if __name__ == "__main__":
    main()
