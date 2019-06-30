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

    # editor = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    initiative = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Initiative.objects.all(), required=False)
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
        fields = ['editor',
                  'initiative',
                  'language',
                  'place',
                  'title',
                  'problem',
                  'solution',
                  'outcome',
                  'categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['editor'].widget = forms.HiddenInput()
        self.fields['editor'].required = True
        # self.fields['initiative'].widget = forms.HiddenInput()
        # self.fields['initiative'].required = False
        self.fields['categories'].initial = \
            self.instance.initiative_language.initiative.categories.all() \
                if self.instance and self.instance.pk else None

    def save(self, commit=True):
        version = super().save(commit=False)
        if commit:
            with transaction.atomic():
                initiative = self.cleaned_data['initiative']
                if not initiative:
                    h = {'place_' + f: self.cleaned_data['place'][f] for f in self.cleaned_data['place'].keys()}
                    initiative = Initiative.objects.create(**h)
                if initiative.add_version(version, self.cleaned_data['language']):
                    if 'categories' in self.cleaned_data:  # no such in Translation
                        try:
                            for category in self.cleaned_data['categories']:
                                initiative.categories.add(category)
                        except IntegrityError as e:
                            raise ValidationError(e)
        return version


class TranslateInitiativeForm(InitiativeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('categories')
        self.fields.pop('place')


class VoteForm(forms.Form):
    vote = VoteField(widget=VoteWidget(vote_for_text=_("Votes for"),
                                       vote_against_text=_("Votes against")))
    vote_being_spam = VoteField(widget=VoteWidget(vote_for_text=_("Votes for being SPAM"),
                                vote_against_text=_("Votes against being SPAM")))

    def __init__(self, request, initiative, version):
        initial = {'vote': {'request': request,
                            'pool': 'main',
                            'initiative_pk': initiative and initiative.pk,
                            'for': initiative and initiative.votes_for,
                            'against': initiative and initiative.votes_against},
                   'vote_being_spam': {'request': request,
                                       'pool': 'spam',
                                       'initiative_pk': version and version.pk,
                                       'for': version and version.votes_for_being_spam,
                                       'against': version and version.votes_against_being_spam}}

        for field_name in 'vote', 'vote_being_spam':
            self.rectify_field(initial, field_name)

        return super().__init__(initial=initial)

    def rectify_field(self, initial, field_name):
        with transaction.atomic():
            # TODO: Don't calculate these counts when doing voting
            votes_for = initial[field_name]['for'] and initial[field_name]['for'].count()
            votes_against = initial[field_name]['against'] and initial[field_name]['against'].count()
            myself_for = initial[field_name]['request'].user in initial[field_name]['for'].all() if \
                initial[field_name]['for'] and initial[field_name]['request'].user in initial[field_name]['for'].all() else False
            myself_against = initial[field_name]['request'].user in initial[field_name]['against'].all() if \
                initial[field_name]['against'] and initial[field_name]['request'].user in initial[field_name]['against'].all() else False

        if myself_for:
            votes_for -= 1
        if myself_against:
            votes_against -= 1

        initial[field_name]['votes_for'] = votes_for
        initial[field_name]['votes_against'] = votes_against
        initial[field_name]['myself_for'] = myself_for
        initial[field_name]['myself_against'] = myself_against
