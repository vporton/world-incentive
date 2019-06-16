from django import forms

from core.widgets import PlaceWidget


class PlaceFormField(forms.MultiValueField):
    widget = PlaceWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField(),
                       forms.fields.ChoiceField()]
        super().__init__(list_fields, *args, **kwargs)

    # def compress(self, values):
    #     return pickle.dumps(values)
