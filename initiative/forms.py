from django import forms
from django.conf import settings
from django.forms import ChoiceField
from django.utils.translation import gettext as _
import languages.languages
from languages.forms import LanguageField

from core.fields import PlaceFormField
from initiative.models import InitiativeVersion


class CreateInitiativePromptForm(forms.Form):
    language = ChoiceField(choices=languages.languages.LANGUAGES,
                           widget=forms.Select(),
                           label=_("Initiative language"),
                           help_text=_("More languages can be added later."))


class InitiativeForm(forms.ModelForm):
    required_css_class = 'required'

    language = LanguageField(choices=languages.languages.LANGUAGES,
                             label=_("Initiative language"),
                             help_text=_("More languages can be added later."))
    place = PlaceFormField(required=False,
                           help_text=_("Enter nothing for distributing the initiative to the entire world."))

    class Meta:
        model = InitiativeVersion
        fields = ['language',
                  'place',
                  'title',
                  'problem',
                  'solution',
                  'outcome']
