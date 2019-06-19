from django.shortcuts import render
from django.views import View

from initiative.forms import InitiativeForm


class MainPage(View):
    def get(self, request):
        return render(request, 'main/mainpage.html')
