from django.db import models
from django.utils.translation import gettext as _
from languages.fields import LanguageField

import core.models


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

    place = core.models.PlaceField()
    # level = models.SmallIntegerField(_("Initiative level"))  # core.RegionLevel

    votes_for = models.BigIntegerField(_("Votes for"), default=0)
    votes_against = models.BigIntegerField(_("Votes against"), default=0)


class InitiativeLanguage(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='languages')
    language = LanguageField(db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['initiative', 'language'], name='unique_initiative_language'),
        ]


class InitiativeVersion(models.Model):
    initiative_language = models.ForeignKey(InitiativeLanguage, on_delete=models.CASCADE, related_name='versions')

    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255, blank=False)
    problem = models.TextField(blank=False)
    solution = models.TextField(blank=False)
    outcome = models.TextField(blank=False)

    categories = models.ManyToManyField(InitiativeCategory)
