from django import forms
from django.forms import ChoiceField, CheckboxSelectMultiple
from django.utils.translation import gettext as _
import languages.languages
from languages.forms import LanguageField

from core.fields import PlaceFormField
from initiative.models import InitiativeVersion, InitiativeCategory


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
    categories = forms.ModelMultipleChoiceField(queryset=InitiativeCategory.objects.all(),
                                                widget=CheckboxSelectMultiple,
                                                required=False)

    class Meta:
        model = InitiativeVersion
        fields = ['language',
                  'place',
                  'title',
                  'problem',
                  'solution',
                  'outcome']
