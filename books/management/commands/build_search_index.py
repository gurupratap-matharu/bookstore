import json

from django.conf import settings
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):

    """
    Management commands which build the search index json file.
    """

    help = "Exports items data in a json format to build autocomplete search"

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def danger(self, msg):
        self.stdout.write(self.style.HTTP_BAD_REQUEST(msg))

    def handle(self, *args, **options):
        static = (
            settings.STATICFILES_DIRS[0] if settings.DEBUG else settings.STATIC_ROOT
        )
        folder = static / "assets" / "index"
        folder.mkdir(parents=True, exist_ok=True)
        
        index_path = folder / "books.json"
        
        self.success(f"🔍 Building search index at {index_path}...")

        books = list(Book.objects.values_list("title", flat=True))
        with open(index_path, "w") as f:
            f.write(json.dumps(books))

        self.success("All Done 💅🏻✨💫")
