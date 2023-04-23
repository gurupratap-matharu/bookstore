import logging
from urllib.parse import urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

from bookstore_project.decorators import timeit

logger = logging.getLogger(__name__)


class BaseScraper:
    """
    Abstract class that implements the basic interface of a scraper.
    """

    url = None

    def __init__(self):
        self.base_url = self.build_base_url(self.url)

    def run(self):
        raise NotImplementedError("Subclass should implement this method...")

    @timeit
    def get_soup(self, url):
        """
        Hit the url and build a beautiful soup object
        """

        html = urlopen(url)  # nosec
        return BeautifulSoup(html, "html.parser")

    def build_base_url(self, url=None):
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

    def build_full_url(self, path, leading_slash=False):
        """
        Build a full url for any internal path of a site.
        """
        url = f"{self.base_url}/{path}" if leading_slash else f"{self.base_url}{path}"
        return url

    def get_items(self, bs=None):
        """
        Interface to get a list of urls for all the items on the page.
        """

        return NotImplementedError("Subclass should implement this method...")

    def get_item(self, url=None):
        """
        Interface method to get a single item from its url.
        """

        return NotImplementedError("Subclass should implement this method...")

    def save_item_to_db(self, item=None):
        logger.info("saving item %s to db..." % item)
