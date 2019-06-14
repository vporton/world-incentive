import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from incentive.models import *


class Command(BaseCommand):
    help = 'Updates DB for a list of countries/cities'

    def handle(self, *args, **options):
        with open(settings.BASE_DIR + '/data/countriesToCities.json') as file:
            data = json.load(file)
        with transaction.atomic():  # for speed
            for country_name, cities in data.items():
                country, _ = Country.objects.get_or_create(name=country_name)
                for city_name in cities:
                    City.objects.get_or_create(country=country, name=city_name)
        print("%d countries, %d cities." % (Country.objects.count(), City.objects.count()))
