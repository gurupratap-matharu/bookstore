from django.core.management.base import BaseCommand

from books.scrapers.sedici import SediciScraper


class Command(BaseCommand):

    """
    Management commands which runs the sedici scraper.
    """

    help = "Runs the Sedici Scraper"

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def danger(self, msg):
        self.stdout.write(self.style.HTTP_BAD_REQUEST(msg))

    def handle(self, *args, **options):
        self.success("🕷️ Starting the Sedici Scraper....")

        SediciScraper().run()

        self.success("All Done 💅🏻✨💫")
