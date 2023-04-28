import random
import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
    Management commands which makes django sleep for a while
    """

    help = "Take an nap for some seconds"

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        secs = random.randint(5, 10)

        self.success(f"😴 Veer taking a nap for {secs} seconds...")

        time.sleep(secs)

        self.success("🙂 That was a good nap")
