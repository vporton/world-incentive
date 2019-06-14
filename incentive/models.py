from django.db import models
from django.utils.translation import gettext as _
from languages.fields import LanguageField


class Country(models.Model):
    name = models.CharField(unique=True, max_length=255)


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    constraints = [
        models.UniqueConstraint(fields=['name', 'country'], name='city_unique')
    ]


class InitiativeCategory(models.Model):
    name = models.CharField(max_length=255)


class InitiativeImage(models.Model):
    initiative = models.ForeignKey('Initiative', on_delete=models.CASCADE)
    image = models.FileField(_("Attached image"))


class InitiativeFile(models.Model):
    initiative = models.ForeignKey('Initiative', on_delete=models.CASCADE)
    file = models.FileField(_("Attached file"))


class Initiative(models.Model):
    LEVEL_WORLD = 0
    # LEVEL_UNION = 1
    LEVEL_COUNTRY = 2
    # LEVEL_REGION = 3
    LEVEL_CITY = 4
    # LEVEL_MUNICIPAL = 5

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    level = models.SmallIntegerField(_("Initiative level"))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    language = LanguageField()

    title = models.CharField(max_length=255)
    problem = models.TextField()
    solution = models.TextField()
    outcome = models.TextField()

    categories = models.ManyToManyField(InitiativeCategory)

    votes_for = models.BigIntegerField(_("Votes for"))
    votes_against = models.BigIntegerField(_("Votes against"))
