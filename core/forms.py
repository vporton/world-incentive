from django import forms
from django.conf import settings
from django.forms import ChoiceField
from django.utils.translation import gettext as _


class LanguageChoiceForm(forms.Form):
    # language = ChoiceField(choices=[('en', _("English")), (('ru', _("Russian")))],
    language = ChoiceField(choices=settings.LANGUAGES,
                           initial='en',
                           widget=forms.Select(attrs={'onchange': 'set_language(this.value)'}))