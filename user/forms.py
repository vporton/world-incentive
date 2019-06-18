from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.utils.translation import gettext as _

from core.fields import PlaceFormField, LanguagesListField
from user.models import User


class AccountFormMixin(object):
    def init_account_form(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            self.initial['place'] = instance.place._composite_field.value_from_object(instance)

    def save(self, commit=True):
        value = super().save(False)
        for f in self.cleaned_data['place'].keys():
            setattr(value.place, f, self.cleaned_data['place'][f])
        if commit:
            value.save()
        return value


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
