# proxin

proxin is a Python tool for extracting proxies from various online sources.

## Features

- Extracts proxies from multiple websites
- Modular design for easy addition of new proxy sources
- Removes duplicate proxies
- Command-line interface for easy usage

## Installation

To install proxin, clone the repository and install it using pip:

```
git clone https://github.com/444995/proxin
cd proxin
pip install .
```

## Usage

You can use proxin from the command line:

```
proxin --url <url>
```

Replace `<url>` with the URL of the proxy list website you want to scrape. Batch processing will be added in the future.

## Example

Here's an example of how to use proxin to extract proxies from geonode.com:

```
proxin --url https://iproyal.com/free-proxy-list
```

This will fetch and display proxies from [iproyal.com](https://iproyal.com)

## Contributing

Contributions are welcome! Please feel free to submit a ?R.

To add support for a new proxy list website:

1. Create a new file in the `proxin/sites` directory (e.g., `newsite.py`)
2. Define a new class that inherits from `BaseSite`
3. Implement the `extract_proxies` method
4. Add the site's URL as a class attribute

Example:

```python
from .base_site import BaseSite
from ..requester import Requester

class NewSite(BaseSite):
    url = "https://newproxysite.com"

    def __init__(self):
        self.requester = Requester()

    def extract_proxies(self):
        # Implement proxy extraction logic here
        pass
```

## License

This project is licensed under the MIT License.
