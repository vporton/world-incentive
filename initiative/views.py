from django.shortcuts import render
from django.utils.translation import get_language_from_request
from django.views import View

from initiative.forms import CreateInitiativePromptForm


class CreateInitiativePromptView(View):
    def get(self, request):
        language = get_language_from_request(request)
        form = CreateInitiativePromptForm(initial={'language': language})
        return render(request, 'initiative/create-initiative-prompt.html', {'form': form})