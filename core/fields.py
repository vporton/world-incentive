from django import forms
from django.core.exceptions import ValidationError
import cities.models

import core.models
from core.widgets import PlaceWidget
from django.utils.translation import gettext as _


class PlaceFormField(forms.MultiValueField):
    widget = PlaceWidget

    @staticmethod
    def _my_validate(value):
        print(value.__dict__)  # FIXME
        if value.region and value.region.country != value.country or \
                value.subregion and value.subregion.region != value.region or \
                value.city and value.city.subregion != value.subregion or \
                value.district and value.district.city != value.city:
            raise ValidationError(_("Wrong places hierarchy"))

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.IntegerField(),
                       forms.fields.IntegerField(),
                       forms.fields.IntegerField(),
                       forms.fields.IntegerField(),
                       forms.fields.IntegerField()]
        super().__init__(list_fields, *args, **kwargs)
        self.validators.append(PlaceFormField._my_validate)

    def compress(self, values):
        # TODO: What to do if the PK doesn't refer to an object?
        return core.models.PlaceField(default={'country': values[0] and cities.models.Country.objects.get(pk=values[0]),
                                               'region': values[1] and cities.models.Region.objects.get(pk=values[1]),
                                               'subregion': values[2] and cities.models.Subregion.objects.get(pk=values[2]),
                                               'city': values[3] and cities.models.City.objects.get(pk=values[3]),
                                               'district': values[4] and cities.models.District.objects.get(pk=values[4])})
