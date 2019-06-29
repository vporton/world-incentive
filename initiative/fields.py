from django import forms

from initiative.widgets import VoteWidget


class VoteField(forms.Field):
    widget = VoteWidget
