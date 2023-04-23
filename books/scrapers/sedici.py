import json
import logging
from pathlib import Path
from urllib.parse import unquote_plus

from books.models import Book
from bookstore_project.decorators import timeit

from .base import BaseScraper

logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent


class SediciScraper(BaseScraper):
    # url = (
    #     "http://sedici.unlp.edu.ar/discover?"
    #     "filtertype=type&filter_relational_operator=equals"
    #     "&filter=Libro&sort_by=dc.date.accessioned_dt&order=desc"
    # )

    # This 40 results per page seems to be the fastest
    url = (
        "http://sedici.unlp.edu.ar/discover"
        "?search-result=true&query=&current-scope=&filtertype_0=type"
        "&filter_relational_operator_0=equals&filter_0=Libro"
        "&sort_by=dc.date.accessioned_dt&order=desc&rpp=40"
    )

    item_urls = set()
    items_data = list()

    item_urls_filename = str(CURRENT_DIR / "sedici_item_urls.txt")
    item_data_filename = str(CURRENT_DIR / "sedici_items.json")

    @timeit
    def run(self):
        logger.info("running sedici scraper...")

        url = self.url

        while url:
            # Get all item (books) urls from a page
            bs = self.get_soup(url)
            self.get_items(bs)

            # Update url to next page
            url = self.get_next_page_link(bs)

        # Save all item urls to a file
        self.save_item_urls()

        # Retrieve each item from its url and save to DB
        for item_url in self.item_urls:
            item = self.get_item(item_url)
            self.save_item_to_db(item=item)

        # Save all items data to a json file
        self.save_items_data()

        return self.item_urls

    def get_items(self, bs):
        links = bs.find("ul", {"class": "ds-artifact-list"}).find_all("a")

        for link in links:
            link_path = link.attrs.get("href", "")
            item_url = self.build_full_url(link_path)

            self.item_urls.add(item_url)

        return self.item_urls

    @timeit
    def get_item(self, item_url):
        logger.info("fetching item: %s" % item_url)

        item_data = dict()

        bs = self.get_soup(url=item_url)
        item = bs.find(class_="item-summary-view-metadata")

        item_data["title"] = item.find("h1").get_text().strip()

        authors = [
            sibling.text.strip()
            for sibling in item.find(
                class_="simple-item-view-authors"
            ).span.next_siblings
        ]
        item_data["authors"] = [
            name.replace("|", "").strip() for name in authors if name != ""
        ]

        item_data["issue_date"] = item.find(class_="date-issued").get_text().strip()

        item_data["item_type"] = "".join(
            s.text.strip() for s in item.find(class_="subtype").span.next_siblings
        )

        description_tag = item.find(class_="simple-item-view-description")
        item_data["description"] = description_tag.p.get_text().strip()

        item_data["language"] = self.extract(item, "language")
        item_data["publisher"] = self.extract(item, "publisher")
        item_data["origin"] = self.extract(item, "originInfo")
        item_data["isbn"] = self.extract(item, "identifier-isbn")
        item_data["subjects"] = self.extract(item, "subject-materias")
        item_data["created_since"] = self.extract(item, "date-accessioned")
        item_data["available_since"] = self.extract(item, "date-available")

        thumbnail_path = item.find(class_="image-link").img.attrs.get("src")
        item_data["thumbnail"] = self.build_full_url(thumbnail_path)

        metadata_tag = item.find(class_="file-metadata")
        span_link, span_size, span_format = metadata_tag.find_all("span")

        download_path = span_link.a.attrs.get("href")

        item_data["download_link"] = self.build_full_url(download_path)
        item_data["file_size"] = span_size.get_text().strip()
        item_data["file_format"] = span_format.get_text().strip()

        google_scholar_raw_url = item.find(id="google-scholar-search").a.attrs.get(
            "href"
        )
        base_search_net_raw_url = item.find(id="base-search-net").a.attrs.get("href")

        item_data["google_scholar"] = unquote_plus(google_scholar_raw_url)
        item_data["base_search_net"] = unquote_plus(base_search_net_raw_url)

        self.items_data.append(item_data)

        return item_data

    def get_next_page_link(self, bs=None):
        """
        Extract the link to the next page if any.
        """

        try:
            next_page_path = bs.find(class_="next-page-link").a.attrs.get("href")
            next_page_link = self.build_full_url(next_page_path, leading_slash=True)
            logger.info("next_page_link: %s" % next_page_link)

        except AttributeError:
            next_page_link = ""
            logger.info("📃 No next page exists...")

        return next_page_link

    def save_item_urls(self):
        """
        Write all item urls to a simple text file.
        """

        logger.info("📝 writing item urls to file...")

        with open(self.item_urls_filename, "w") as f:
            for line in self.item_urls:
                f.write(f"{line}\n")

    def save_items_data(self):
        """
        Write all items (books) data to a local file for later perusal
        """

        logger.info("📝 writing items data to file...")

        with open(self.item_data_filename, "w") as f:
            f.write(json.dumps(self.items_data))

    def extract(self, item, klass):
        """
        Helper method to pull out common info for an item.
        """

        try:
            value = (
                item.find(class_=klass).find(class_="metadata-value").get_text().strip()
            )

        except AttributeError:
            value = ""

        return value

    def save_item_to_db(self, item):
        """
        Saves an item (book) to the DB if it doesn't exists.
        If the object already exists do nothing simply fetch and return it to avoid duplication.
        """

        obj, created = Book.objects.get_or_create(
            title=item["title"],
            description=item["description"],
            link=item["download_link"],
        )

        logger.info("created:%s item:%s..." % (created, obj))

        return obj
