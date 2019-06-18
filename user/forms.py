from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.forms import ModelForm, forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.utils.translation import gettext as _

from core.fields import PlaceFormField, LanguagesListField
from user.models import User, UserLanguage


class AccountFormMixin(object):
    def init_account_form(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            self.initial['place'] = instance.place._composite_field.value_from_object(instance)
            self.initial['languages'] = instance.languages.all().values_list('language', flat=True)

    def save(self, commit=True):
        value = super().save(False)
        for f in self.cleaned_data['place'].keys():
            setattr(value.place, f, self.cleaned_data['place'][f])
        if commit:
            with transaction.atomic():
                value.save()
                value.languages.all().delete()  # TODO: Don't run this on creation of new users?
                # Bulk creation does not work for OrderedModel.
                # UserLanguage.objects.bulk_create(
                #     [UserLanguage(user=value, language=language)
                #      for language in value.languages])
                try:
                    for language in self.cleaned_data['languages']:
                        UserLanguage.objects.create(user=value, language=language)
                except IntegrityError as e:
                    raise ValidationError(e)
        return value

    def clean_languages(self):
        data = self.cleaned_data['languages']
        if len(data) == 0:
            raise forms.ValidationError(_("Specify at least one language."))
        if len(data) > len(set(data)):
            raise forms.ValidationError(_("Each language can be specified at most once."))
        return data


class MyUserCreationForm(AccountFormMixin, UserCreationForm):
    required_css_class = 'required'

    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    place = PlaceFormField(required=False)
    languages = LanguagesListField(label=_("User's languages"), help_text=_("In order of preference"))

    class Meta:
        model = User
        fields = ['place',
                  'username',
                  'password1',
                  'password2',
                  'email',
                  'first_name',
                  'last_name',
                  'languages',
                  'ssh_pubkey',
                  'pgp_pubkey',
                  'show_email',
                  'show_keys',
                  'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_account_form(*args, **kwargs)


class AccountForm(AccountFormMixin, ModelForm):
    required_css_class = 'required'

    place = PlaceFormField(required=False)
    languages = LanguagesListField(label=_("User's languages"), help_text=_("In order of preference"))

    class Meta:
        model = User
        fields = ['place',
                  'username',
                  'first_name',
                  'last_name',
                  'languages',
                  'ssh_pubkey',
                  'pgp_pubkey',
                  'show_email',
                  'show_keys']
        required = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_account_form(*args, **kwargs)
