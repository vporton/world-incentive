import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request
from django.views import View
from django.utils.translation import gettext as _

from initiative.forms import CreateInitiativePromptForm, InitiativeForm
from initiative.models import InitiativeLanguage


class ShowInitiativeView(View):
    def get(self, request, initiative_pk):
        lang = request.GET.get('lang', '')
        language_codes = lang.split(',')

        lang_obj = None
        for language_code in language_codes:
            try:
                lang_obj = InitiativeLanguage.objects.get(initiative__pk=initiative_pk, language=language_code)
            except InitiativeLanguage.DoesNotExist:
                pass
            else:
                break

        version = lang_obj.last_version if lang_obj else None

        problem = version and mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p']))
        solution = version and mark_safe(bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p']))
        outcome = version and mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p']))
        return render(request, 'initiative/view.html', {'version': version,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome})


class CreateInitiativePromptView(LoginRequiredMixin, View):
    def get(self, request):
        language = get_language_from_request(request)
        form = CreateInitiativePromptForm(initial={'language': language})
        return render(request, 'initiative/create-initiative-prompt.html', {'form': form})


class CreateInitiativeView(LoginRequiredMixin, View):
    def get(self, request):
        language = request.GET.get('language', 'en')
        form = InitiativeForm(initial={'language': language})
        return render(request, 'initiative/initiative-form.html', {'form': form})

    def post(self, request):
        form = InitiativeForm(request.POST)
        form.fields['editor'] = request.user
        form.save()
        return render(request, 'initiative/initiative-form.html', {'form': form})  # FIXME
