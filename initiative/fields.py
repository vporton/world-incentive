from django import forms
from django.db import transaction

from initiative.widgets import VoteWidget


class VoteField(forms.Field):
    widget = VoteWidget

    @transaction.atomic
    def vote(self, request, value, against, reclaim):
        if reclaim:
            if against:
                value['against'].remove(request.user)
            else:
                value['for'].remove(request.user)
        else:
            if against:
                value['against'].add(request.user)
                value['for'].remove(request.user)
            else:
                value['for'].add(request.user)
                value['against'].remove(request.user)
