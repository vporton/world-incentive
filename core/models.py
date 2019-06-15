from composite_field import CompositeField
from django.db import models


class PlaceField(CompositeField):
    country = models.ForeignKey('cities.Country', on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey('cities.Region', on_delete=models.SET_NULL, null=True)
    subregion = models.ForeignKey('cities.Subregion', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('cities.City', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('cities.District', on_delete=models.SET_NULL, null=True)


class RegionLevel(object):
    LEVEL_WORLD = 0
    # LEVEL_UNION = 1
    LEVEL_COUNTRY = 2
    # LEVEL_REGION = 3
    LEVEL_CITY = 4
    # LEVEL_MUNICIPAL = 5
