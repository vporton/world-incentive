import django.contrib.auth.models
from django.db import models


class User(django.contrib.auth.models.AbstractUser):
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('core.City', on_delete=models.SET_NULL, null=True)

    ssh_pubkey = models.TextField("SSH public key", help_text="Leave empty if not sure", blank=True)
    pgp_pubkey = models.TextField("PGP (mail) public key", help_text="Leave empty if not sure", blank=True)
    show_email = models.BooleanField("Show email publicly", default=False)
    show_keys = models.BooleanField("Show public keys publicly", default=False)
