from django import forms
from django.core.exceptions import ValidationError

import core.models
from core.widgets import PlaceWidget
from django.utils.translation import gettext as _


class PlaceFormField(forms.MultiValueField):
    widget = PlaceWidget

    @staticmethod
    def _my_validate(value):
        if value.region and value.region.country != value.country or \
                value.subregion and value.subregion.region != value.region or \
                value.city and value.city.subregion != value.subregion or \
                value.district and value.district.city != value.city:
            raise ValidationError(_("Wrong places hierarchy"))

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField()]
        super().__init__(list_fields, *args, **kwargs)
        self.validators.append(PlaceFormField._my_validate)

    def compress(self, values):
        return core.models.PlaceField(*values)
