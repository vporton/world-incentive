from cities.models import Country
from django.forms import widgets


class PlaceWidget(widgets.MultiWidget):
    template_name = 'core/widgets/placewidget.html'

    class Media:
        js = ('js/placewidget.js',)

    def __init__(self, attrs=None):
        _widgets = (
            widgets.Select(choices=[('', '-')] + [(c.pk, c.name) for c in Country.objects.all().order_by('name')],
                           attrs={'onchange': "update_places_list(1)", **(attrs or {})}),
            widgets.Select(choices=[('', '-')],
                           attrs={'onchange': "update_places_list(2)", **(attrs or {})}),
            widgets.Select(choices=[('', '-')],
                           attrs={'onchange': "update_places_list(3)", **(attrs or {})}),
            widgets.Select(choices=[('', '-')],
                           attrs={'onchange': "update_places_list(4)", **(attrs or {})}),
            widgets.Select(choices=[('', '-')])
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value['country'].pk if value['country'] else None,
                    value['region'].pk if value['region'] else None,
                    value['subregion'].pk if value['subregion'] else None,
                    value['city'].pk if value['city'] else None,
                    value['district'].pk if value['district'] else None]
        return [None, None, None, None, None]
