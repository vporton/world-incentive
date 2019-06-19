from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language_from_request
from django.views import View
from django.utils.translation import gettext as _

from initiative.forms import CreateInitiativePromptForm, InitiativeForm


class CreateInitiativePromptView(View):
    def get(self, request):
        language = get_language_from_request(request)
        form = CreateInitiativePromptForm(initial={'language': language})
        return render(request, 'initiative/create-initiative-prompt.html', {'form': form})


class CreateInitiativeView(View):
    def get(self, request):
        language = request.GET.get('language', 'en')
        form = InitiativeForm(initial={'language': language})
        return render(request, 'initiative/initiative-form.html', {'form': form})

    def post(self, request):
        form = InitiativeForm(request.POST)
        form.save()
        return render(request, 'initiative/initiative-form.html', {'form': form})  # FIXME
