from django.db import models
from django.utils.translation import gettext as _
from languages.fields import LanguageField


class InitiativeCategory(models.Model):
    name = models.CharField(max_length=255)


class InitiativeImage(models.Model):
    initiative = models.ForeignKey('Initiative', on_delete=models.CASCADE)
    image = models.FileField(_("Attached image"))


class InitiativeFile(models.Model):
    initiative = models.ForeignKey('Initiative', on_delete=models.CASCADE)
    file = models.FileField(_("Attached file"))


class Initiative(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    level = models.SmallIntegerField(_("Initiative level"))  # core.RegionLevel
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('core.City', on_delete=models.SET_NULL, null=True)

    language = LanguageField()

    title = models.CharField(max_length=255)
    problem = models.TextField()
    solution = models.TextField()
    outcome = models.TextField()

    categories = models.ManyToManyField(InitiativeCategory)

    votes_for = models.BigIntegerField(_("Votes for"))
    votes_against = models.BigIntegerField(_("Votes against"))
