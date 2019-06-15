import django.contrib.auth.models
from django.db import models


class User(django.contrib.auth.models.AbstractUser):
    ssh_pubkey = models.TextField("SSH public key", help_text="Leave empty if not sure", blank=True)
    pgp_pubkey = models.TextField("PGP (mail) public key", help_text="Leave empty if not sure", blank=True)
    show_email = models.BooleanField("Show email publicly", default=False)
    show_keys = models.BooleanField("Show public keys publicly", default=False)
