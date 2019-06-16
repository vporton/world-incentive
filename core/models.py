import cities.models
from composite_field import CompositeField
from django.db import models

import core.fields


class PlaceField(CompositeField):
    country = models.ForeignKey('cities.Country', on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey('cities.Region', on_delete=models.SET_NULL, null=True)
    subregion = models.ForeignKey('cities.Subregion', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('cities.City', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('cities.District', on_delete=models.SET_NULL, null=True)

    def formfield(self, **kwargs):
        defaults = {'form_class': core.fields.PlaceFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class RegionLevel(object):
    LEVEL_WORLD = 0
    LEVEL_COUNTRY = 1
    LEVEL_REGION = 2
    LEVEL_SUBREGION = 3
    LEVEL_CITY = 4
    LEVEL_DISTRICT = 5

    @staticmethod
    def get_model(level):
        return {
            RegionLevel.LEVEL_COUNTRY: cities.models.Country,
            RegionLevel.LEVEL_REGION: cities.models.Region,
            RegionLevel.LEVEL_SUBREGION: cities.models.Subregion,
            RegionLevel.LEVEL_CITY: cities.models.City,
            RegionLevel.LEVEL_DISTRICT: cities.models.District,
        }[level]