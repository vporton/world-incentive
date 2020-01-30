from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
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

    categories = models.ManyToManyField(InitiativeCategory)

    votes_for = models.ManyToManyField('user.User',
                                       verbose_name=_("Votes for"),
                                       related_name='voters_for')
    votes_against = models.ManyToManyField('user.User',
                                           verbose_name=_("Votes against"),
                                           related_name='voters_against')

    def last_version(self, language):
        try:
            lang_obj = self.languages.get(language=language)
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
                lang_obj.save()
                self.updated = timezone.now()
            return True

    def first_of_specified_languages(self, language_codes):
        lang_obj = None
        for language_code in language_codes:
            try:
                lang_obj = InitiativeLanguage.objects.get(initiative=self, language=language_code)
            except InitiativeLanguage.DoesNotExist:
                pass
            else:
                break
        return lang_obj

    def version_in_specified_languages(self, language_codes):
        lang_obj = self.first_of_specified_languages(language_codes)
        return lang_obj.last_version if lang_obj else None

    # TODO: slow
    @property
    def spam(self):
        return not self.select_related('languages__versions').exists(spam=False)


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

    def get_absolute_url(self):
        return reverse('initiative:view', args=[self.initiative.pk]) + '?lang=' + str(self.language)

    def __str__(self):
        return self.language

class InitiativeVersion(models.Model):
    initiative_language = models.ForeignKey(InitiativeLanguage, on_delete=models.CASCADE, related_name='versions')

    created = models.DateTimeField(auto_now_add=True)

    editor = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=255, blank=False)
    problem = models.TextField(blank=False)
    solution = models.TextField(blank=False)
    outcome = models.TextField(blank=False)

    votes_for_being_spam = models.ManyToManyField('user.User',
                                                  verbose_name=_("Votes for being SPAM"),
                                                  related_name='voters_for_being_spam')
    votes_against_being_spam = models.ManyToManyField('user.User',
                                                      verbose_name=_("Votes against being SPAM"),
                                                      related_name='voters_against_being_spam')
    spam = models.BooleanField(default=False)

    def __str__(self):
        return "[%s] %s" % (self.initiative_language, self.title)

    def __eq__(self, other):
        if other is None:
            return False
        if self.title != other.title or \
                self.problem != other.problem or \
                self.solution != other.solution or \
                self.outcome != other.outcome:
            return False
        return True

    def get_absolute_url(self):
        return reverse('initiative:view-old', args=[self.pk])
