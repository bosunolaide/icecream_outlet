from django.core.management.base import BaseCommand
from recommendations.ml.train_model import train_flavour_recommender

class Command(BaseCommand):
    help = "Train and save the flavour recommendation model"

    def handle(self, *args, **options):
        train_flavour_recommender()
