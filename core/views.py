import html

from django import views
from django.http import HttpResponse
from django.utils.translation import gettext as _

from core.models import RegionLevel


class CitiesAjaxView(views.View):
    def get(self, request, level, parent_pk):
        try:
            klass = RegionLevel.get_model(level + 1)
            parent_rel = {
                RegionLevel.LEVEL_COUNTRY: 'country_id',
                RegionLevel.LEVEL_REGION: 'region_id',
                RegionLevel.LEVEL_SUBREGION: 'subregion_id',
                RegionLevel.LEVEL_CITY: 'city_id',
            }[level]
        except KeyError:
            return HttpResponse(_("Wrong level"), status=400)
        lst = klass.objects.filter(**{parent_rel: parent_pk}).order_by('name').only('pk', 'name')
        return HttpResponse("\n".join(["<option value='%d'>%s</option>" % (item.pk, html.escape(item.name)) \
                                       for item in lst]))
