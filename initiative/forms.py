from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.forms import ChoiceField, CheckboxSelectMultiple, Field
from django.utils.translation import gettext as _
import languages.languages
from languages.forms import LanguageField

from core.fields import PlaceFormField
from initiative.fields import VoteField
from initiative.models import InitiativeVersion, InitiativeCategory, InitiativeLanguage, Initiative
from initiative.widgets import VoteWidget


class CreateInitiativePromptForm(forms.Form):
    language = ChoiceField(choices=languages.languages.LANGUAGES,
                           widget=forms.Select(),
                           label=_("Initiative language"),
                           help_text=_("More languages can be added later."))


class InitiativeForm(forms.ModelForm):
    required_css_class = 'required'

    initiative = forms.IntegerField(widget=forms.HiddenInput(), required=False)
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
        fields = ['initiative',
                  'language',
                  'place',
                  'title',
                  'problem',
                  'solution',
                  'outcome']

    def save(self, commit=True):
        version = super().save(commit=False)
        if commit:
            with transaction.atomic():
                initiative_id = self.cleaned_data['initiative']
                if initiative_id:
                    initiative = Initiative.objects.get(pk=initiative_id)
                else:
                    h = {'place_' + f: self.cleaned_data['place'][f] for f in self.cleaned_data['place'].keys()}
                    initiative = Initiative.objects.create(**h)
                if initiative.add_version(version, self.cleaned_data['language']):
                    try:
                        for category in self.cleaned_data['categories']:
                            InitiativeLanguage.objects.create(initiative=version, category=category)
                    except IntegrityError as e:
                        raise ValidationError(e)
        return version

class VoteForm(forms.Form):
    vote = VoteField(widget=VoteWidget(vote_for_text=_("Vote for"),
                                       vote_against_text=_("Vote against")))
    vote_being_spam = VoteField(widget=VoteWidget(vote_for_text=_("Vote for being SPAM"),
                                vote_against_text=_("Vote for against SPAM")))

    def __init__(self, *args, initial=None, **kwargs):
        initial2 = initial.copy() if initial is not None else {}
        for field_name in 'vote', 'vote_being_spam':
            self.rectify_field(initial, initial2, field_name)
        return super().__init__(*args, initial2, **kwargs)

    def rectify_field(self, initial, initial2, field_name):
        initial2[field_name]['votes_for'] = initial[field_name]['for'].count()
        initial2[field_name]['votes_against'] = initial[field_name]['against'].count()
