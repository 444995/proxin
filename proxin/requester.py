import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar as cookielib
import gzip
import json
from bs4 import BeautifulSoup

from proxin.logger import logger

class Requester:
    """
    A class to make requests using urllib and handle the responses.
    """
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    def __init__(self):
        """
        Initializes the opener with cookie jar and headers.
        """
        self.cookiejar = cookielib.LWPCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        self.opener.addheaders = [
            ('User-Agent', self.UA),
            ('Accept-Encoding', 'gzip, deflate'),
        ]

    def make_request(self, url, headers=None, params=None, data=None, as_json=True, as_soup=False):
        """
        Makes a request to the given URL using urllib.
        """
        if params:
            url = self._prepare_url(url, params)
        headers = self._prepare_headers(headers, as_json)
        encoded_data = self._prepare_data(data, as_json)

        try:
            request = urllib.request.Request(url, data=encoded_data, headers=headers)
            
            with self.opener.open(request) as response:
                return self._handle_response(response, as_json, as_soup)
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP Error ('{url}'): {e}")
        except Exception as e:
            logger.error(f"Error making request: {e}")

        return None

    @staticmethod
    def _prepare_url(url, params):
        """
        Prepares the URL
        """
        url += '?' + urllib.parse.urlencode(params)
        
        return url
    
    @staticmethod
    def _prepare_headers(headers, as_json):
        """
        Prepares the headers for the request.
        """
        headers = headers or {}
        if as_json:
            headers['Content-Type'] = 'application/json'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        return headers

    @staticmethod
    def _prepare_data(data, as_json):
        """
        Prepares the data for the request, either as JSON or URL-encoded.
        """
        encoded_data = None
        if as_json and data:
            encoded_data = json.dumps(data).encode()
        else:
            encoded_data = urllib.parse.urlencode(data).encode() if data else None
        return encoded_data

    @staticmethod
    def _handle_response(response, as_json, as_soup):
        """
        Handles the response, decompressing if necessary and decoding.
        """
        if response.info().get('Content-Encoding') == 'gzip':
            content = gzip.GzipFile(fileobj=response).read()
        else:
            content = response.read()

        if as_soup:
            return BeautifulSoup(content, 'html.parser')
        
        return json.loads(content) if as_json else content.decode()
