import logging
import time
from urllib.parse import unquote_plus

from .base import BaseScraper

logger = logging.getLogger(__name__)


class SediciScraper(BaseScraper):
    item_urls = set()

    def run(self):
        start = time.time()

        logger.info("running scraper...")

        bs = self.get_soup(self.url)

        item_urls = self.get_items(bs)

        for item_url in item_urls:
            item = self.get_item(item_url)
            self.save_item_to_db(item=item)

        end = time.time()

        logger.info("All done! took %.2f seconds!" % (end - start))

        return self.item_urls

    def get_items(self, bs):
        logger.info("fetching items...")

        links = bs.find("ul", {"class": "ds-artifact-list"}).find_all("a")

        for link in links:
            link_path = link.attrs.get("href", "")
            item_url = self.build_full_url(link_path)

            self.item_urls.add(item_url)

        return self.item_urls

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

        def get_metadata_text(item, klass):
            return (
                item.find(class_=klass).find(class_="metadata-value").get_text().strip()
            )

        item_data["language"] = get_metadata_text(item, "language")
        item_data["publisher"] = get_metadata_text(item, "publisher")
        item_data["origin"] = get_metadata_text(item, "originInfo")
        item_data["isbn"] = get_metadata_text(item, "identifier-isbn")
        item_data["subjects"] = get_metadata_text(item, "subject-materias")
        item_data["created_since"] = get_metadata_text(item, "date-accessioned")
        item_data["available_since"] = get_metadata_text(item, "date-available")

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

        return item_data

    def save_item_to_db(self, item):
        logger.info("saving item %s to db..." % item)
