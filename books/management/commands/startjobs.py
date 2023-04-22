"""
Django management command that triggers the scrapers.
"""

from django.core.management.base import BaseCommand

from books.models import Book
from books.scrapers.sedici import SediciScraper


class Command(BaseCommand):
    """
    Management commands which trigger the scrapers.
    """

    help = "Triggers the scrapers to pull fresh books data"

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def danger(self, msg):
        self.stdout.write(self.style.HTTP_BAD_REQUEST(msg))

    def handle(self, *args, **options):
        sedici = SediciScraper()
        sedici.run()
        books = Book.objects.count()
        self.stdout.write(f"Books: {books}")
