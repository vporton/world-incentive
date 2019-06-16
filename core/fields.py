from django import forms
from django.core.exceptions import ValidationError

from core.models import PlaceField
from core.widgets import PlaceWidget
from django.utils.translation import gettext as _


class PlaceFormField(forms.MultiValueField):
    widget = PlaceWidget

    @staticmethod
    def _my_validate(value):
        if not value.region.country != value.country or \
                not value.subregion.region != value.region or \
                not value.city.subregion != value.subregion or \
                not value.district.city != value.city:
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
        return PlaceField(*values)
