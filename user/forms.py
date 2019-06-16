from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from core.fields import PlaceFormField
from user.models import User


class MyUserCreationForm(UserCreationForm):
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

    def save(self, commit=True):
        value = super().save(commit)
        for f in self.cleaned_data['place'].keys():
            setattr(value.place, f, self.cleaned_data['place'][f])
        return value


class AccountForm(ModelForm):
    required_css_class = 'required'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'ssh_pubkey', 'pgp_pubkey', 'show_email', 'show_keys']
        required = ['username']
