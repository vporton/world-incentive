from cities.models import Country
from django import forms
from django.apps import apps
from django.db import ProgrammingError, OperationalError
from django.forms import widgets
from languages.forms import LanguageField


class PlaceWidget(widgets.MultiWidget):
    template_name = 'core/widgets/placewidget.html'

    class Media:
        js = ('js/placewidget.js',)

    def __init__(self, attrs=None):
        countries = [('', '-')]
        try:
            countries += [(c.pk, c.name) for c in Country.objects.all().order_by('name')]
        except OperationalError:  # not yet migrated (e.g. during migration)
            pass
        _widgets = (
            widgets.Select(choices=countries
                           ,
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


class LanguagesListWidget(forms.Widget):
    template_name = 'core/languages_list.html'

    class Media:
        js = (
            'languages_list/js/languages_list.js',
            # 'jquery-ui-1.12.1.custom/jquery-ui.js',
        )
        css = {
            'screen': ('https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                       'jquery-ui-1.12.1.custom/jquery-ui.min.css'),
        }

    def get_context(self, name, value, attrs):
        d = super().get_context(name, value, attrs)
        d2 = d.copy() if d is not None else {}
        # attrs2 = attrs.copy() if attrs is not None else {}
        # attrs2['required'] = False
        # TODO: _("User language") and _("In order of preference")
        widget = LanguageField().widget
        widget.template_name = 'core/languages_list_item.html'
        d2['empty_value'] = widget.render('language', '')  # TODO: using fixed name 'language' is antinatural
        # d2['empty_value'] = str(LanguageField())  # TODO: using fixed name 'language' is antinatural
        return d2

    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        # Remove the first dummy element
        return data.getlist('language')[1:]