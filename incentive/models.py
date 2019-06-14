from django.db import models


class Country(models.Model):
    name = models.CharField(unique=True, max_length=255)


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    constraints = [
        models.UniqueConstraint(fields=['name', 'country'], name='city_unique')
    ]


# class Incentive(models.Model):
#     pass
