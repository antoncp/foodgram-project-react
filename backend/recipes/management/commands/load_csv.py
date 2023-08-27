from csv import DictReader

from django.apps import apps
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Loads data from .csv files to the DB"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("model")

    def handle(self, *args, **options):
        path = options.get("path")
        model = apps.get_model("recipes", options.get("model"))

        with open(path, "r", encoding="utf-8") as file:
            for row in DictReader(file):
                record = model(**row)
                record.save()
                self.stdout.write(f"Added to a database: {row}")

            self.stdout.write("Import to a database finished")
