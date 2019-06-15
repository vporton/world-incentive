from django import views
from django.shortcuts import render


class CitiesAjaxView(views.View):
    def get(self, request, country_id):
        pass  # cities = City
