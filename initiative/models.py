from itertools import zip_longest
from django.db import models, transaction
from django.utils.translation import gettext as _
from languages.fields import LanguageField

import core.models
from core.misc import LANGUAGE_NAMES


class InitiativeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

    @property
    def last_version(self, language):
        try:
            lang_obj = self.initiativelanguage.get(language=language)
        except InitiativeLanguage.DoesNotExist:
            return None
        return lang_obj.last_version

    def add_version(self, version, language):
        """Return `True` if a new version was created."""
        lang_obj, _ = InitiativeLanguage.objects.get_or_create(initiative=self, language=language)
        if version == lang_obj.last_version:
            return False
        else:
            with transaction.atomic():
                version.initiative = self
                version.initiative_language = lang_obj
                version.save()
                lang_obj.last_version = version
            return True


class InitiativeLanguage(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='languages')
    language = LanguageField(db_index=True)
    last_version = models.ForeignKey('InitiativeVersion', null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['initiative', 'language'], name='unique_initiative_language'),
        ]

    @property
    def language_name(self):
        return LANGUAGE_NAMES[self.language]

class InitiativeVersion(models.Model):
    initiative_language = models.ForeignKey(InitiativeLanguage, on_delete=models.CASCADE, related_name='versions')

    created = models.DateTimeField(auto_now_add=True)

    editor = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=255, blank=False)
    problem = models.TextField(blank=False)
    solution = models.TextField(blank=False)
    outcome = models.TextField(blank=False)

    categories = models.ManyToManyField(InitiativeCategory)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        if other is None:
            return False
        if self.title != other.title or \
                self.problem != other.problem or \
                self.solution != other.solution or \
                self.outcome != other.outcode:
            return False
        cat1 = self.categories.all().order_by('id')
        cat2 = other.categories.all().order_by('id')
        sentinel = object()
        return all(a == b for a, b in zip_longest(cat1, cat2, fillvalue=sentinel))
