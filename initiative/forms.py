from django import forms
from django.conf import settings
from django.forms import ChoiceField
from django.utils.translation import gettext as _
import languages.languages


class CreateInitiativePromptForm(forms.Form):
    language = ChoiceField(choices=languages.languages.LANGUAGES,
                           widget=forms.Select(),
                           label=_("Initiative language"),
                           help_text=_("More languages can be added later."))