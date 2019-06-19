import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request
from django.views import View
from django.utils.translation import gettext as _

from initiative.forms import CreateInitiativePromptForm, InitiativeForm
from initiative.models import InitiativeLanguage, InitiativeVersion


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
        old_versions = lang_obj and lang_obj.versions.order_by('-id')

        problem = version and mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        solution = version and mark_safe(bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        outcome = version and mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        return render(request, 'initiative/view.html', {'version': version,
                                                        'old_versions': old_versions,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome,
                                                        'is_last_version': True})


class ShowInitiativeVersionView(View):
    def get(self, request, version_pk):
        version = get_object_or_404(InitiativeVersion, pk=version_pk)
        lang_obj = version.initiative_language
        old_versions = lang_obj.versions.order_by('-id')

        problem = mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        solution = mark_safe(bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        outcome = mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        return render(request, 'initiative/view.html', {'version': version,
                                                        'old_versions': old_versions,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome,
                                                        'is_last_version': version == lang_obj.last_version})


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
