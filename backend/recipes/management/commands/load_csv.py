from csv import DictReader

from django.apps import apps
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Loads data from .csv files to the DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            nargs="?",
            type=str,
            help="Path to the .csv file",
            default="foodgram_static/ingredients.csv",
        )
        parser.add_argument(
            "model",
            nargs="?",
            type=str,
            help="Name of the model to data insert",
            default="Ingredient",
        )

    def handle(self, *args, **options):
        path = options.get("path")
        model = apps.get_model("recipes", options.get("model"))

        with open(path, "r", encoding="utf-8") as file:
            for row in DictReader(file):
                record = model(**row)
                record.save()
                self.stdout.write(f"Added to a database: {row}")

            self.stdout.write("Import to a database finished")
