from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from core.fields import PlaceFormField
from user.models import User


class AccountFormMixin(object):
    def save(self, commit=True):
        value = super().save(False)
        for f in self.cleaned_data['place'].keys():
            setattr(value.place, f, self.cleaned_data['place'][f])
        if commit:
            value.save()
        return value


class MyUserCreationForm(UserCreationForm, AccountFormMixin):
    required_css_class = 'required'

    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    place = PlaceFormField(required=False)

    class Meta:
        model = User
        fields = ['place',
                  'username',
                  'password1',
                  'password2',
                  'email',
                  'first_name',
                  'last_name',
                  'ssh_pubkey',
                  'pgp_pubkey',
                  'show_email',
                  'show_keys',
                  'captcha']


class AccountForm(ModelForm, AccountFormMixin):
    required_css_class = 'required'

    place = PlaceFormField(required=False)

    class Meta:
        model = User
        fields = ['place',
                  'username',
                  'first_name',
                  'last_name',
                  'ssh_pubkey',
                  'pgp_pubkey',
                  'show_email',
                  'show_keys']
        required = ['username']
