import logging
from urllib.parse import urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BaseScraper:
    """
    Abstract class that implements the basic interface of a scraper.
    """

    def __init__(self, url):
        self.url = url
        self.base_url = self.build_base_url(self.url)

    def run(self):
        raise NotImplementedError("Subclass should implement this method...")

    def get_soup(self, url):
        """
        Hit the url and build a beautiful soup object
        """

        html = urlopen(url)  # nosec
        return BeautifulSoup(html, "html.parser")

    def build_base_url(self, url):
        """
        Strips down any url to its scheme and netlocation only.

        Note this removes all query strings, url params, sub directories but preserves
        subdomains and scheme.

        Examples:
            https://maps.google.com.ar/maps?hl=es-419&tab=wl -> https://maps.google.com.ar
            https://www.google.com.ar/intl/es-419/about/products?tab=wh -> https://www.google.com.ar

        """

        parse = urlparse(url)

        return f"{parse.scheme}://{parse.netloc}"

    def build_full_url(self, path):
        """
        Build a full url for any internal path of a site.
        """

        return f"{self.base_url}{path}"
