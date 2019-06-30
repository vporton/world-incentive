import django.contrib.auth.models
from django.db import models
from django.urls import reverse
from languages.fields import LanguageField
from ordered_model.models import OrderedModel

import core


class UserLanguage(OrderedModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='languages')
    language = LanguageField()
    order_with_respect_to = 'user'

    class Meta(OrderedModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['user', 'language'], name='unique_user_language'),
        ]


class User(django.contrib.auth.models.AbstractUser):
    place = core.models.PlaceField()

    ssh_pubkey = models.TextField("SSH public key", help_text="Leave empty if not sure", blank=True)
    pgp_pubkey = models.TextField("PGP (mail) public key", help_text="Leave empty if not sure", blank=True)
    show_email = models.BooleanField("Show email publicly", default=False)
    show_keys = models.BooleanField("Show public keys publicly", default=False)

    def get_absolute_url(self):
        return reverse('user:profile', args=[self.pk])
