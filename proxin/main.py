import os
import sys
import importlib
from .helpers import get_domain
from .sites.base_site import BaseSite
from .methods.base_method import BaseMethod
from .requester import Requester
from .logger import logger
from .outputter import Outputter

def find_site_class(domain):
    site_path = os.path.join(os.path.dirname(__file__), 'sites')
    for file in os.listdir(site_path):
        if file.endswith('.py') and file != 'base_site.py' and not file.startswith('unfinished__'):
            module_name = f"proxin.sites.{file[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseSite) and attr_value is not BaseSite:
                    if hasattr(attr_value, 'url') and attr_value.url == domain:
                        return attr_value
    return None

def instantiate_site(site_class):
    try:
        site_instance = site_class()
        return site_instance
    except Exception as e:
        raise RuntimeError(f"Error instantiating site class {site_class.__name__}: {e}")

def extract_proxies_from_site(site_instance):
    try:
        return site_instance.extract_proxies()
    except AttributeError as e:
        raise RuntimeError(f"Site class {site_instance.__class__.__name__} does not implement 'extract_proxies': {e}")
    except Exception as e:
        raise RuntimeError(f"Error extracting proxies from site class {site_instance.__class__.__name__}: {e}")

def load_methods():
    methods_path = os.path.join(os.path.dirname(__file__), 'methods')
    methods = []
    for _file in os.listdir(methods_path):
        if _file.endswith('.py') and _file != 'base_method.py':
            module_name = f"proxin.methods.{_file[:-3]}"
            module = importlib.import_module(module_name)
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type) and issubclass(attr_value, BaseMethod) and attr_value is not BaseMethod:
                    methods.append(attr_value)
    return methods

def try_methods(site_data):
    methods = load_methods()
    proxies = []
    for method_class in methods:
        method_instance = method_class(site_data)
        try:
            proxies.extend(method_instance.extract_proxies())
        except AttributeError as e:
            logger.error(f"Method class {method_instance.__class__.__name__} does not implement 'extract_proxies': {e}")
        except Exception as e:
            logger.error(f"Method {method_instance.__class__.__name__} failed: {e}")
    return proxies

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--url':
        print("Usage: proxin --url <url>")
        sys.exit(1)

    url = sys.argv[2]
    domain = get_domain(url)

    site_class = find_site_class(domain)
    proxies = []

    if site_class:
        try:
            site_instance = instantiate_site(site_class)
            proxies = extract_proxies_from_site(site_instance)
        except RuntimeError as e:
            logger.error(e)
            sys.exit(1)
    else:
        requester = Requester()
        try:
            site_data = requester.make_request(url, as_json=False)
            proxies = try_methods(site_data)
        except Exception as e:
            logger.error(f"Error requesting site data: {e}")
            sys.exit(1)

    logger.debug(f"Found {len(proxies)} proxies")
    
    outputter = Outputter(output_folder="results")
    outputter.output_result(proxies)


if __name__ == "__main__":
    main()