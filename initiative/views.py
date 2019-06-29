import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request
from django.views import View
from django.utils.translation import gettext as _

from initiative.forms import CreateInitiativePromptForm, InitiativeForm, VoteForm
from initiative.models import InitiativeLanguage, InitiativeVersion, Initiative, InitiativeCategory


class BaseShowInitiativeView(View):
    def do_get(self, request, version, is_last_version, lang, lang_obj):
        problem = version and mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        solution = version and mark_safe(
            bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        outcome = version and mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))

        initiative = version.initiative_language.initiative
        old_versions = lang_obj and lang_obj.versions.order_by('-id')

        vote_form = VoteForm(request, initiative)

        return render(request, 'initiative/view.html', {'version': version,
                                                        'old_versions': old_versions,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome,
                                                        'is_last_version': is_last_version,
                                                        'lang': lang,
                                                        'vote_form': vote_form})


class ShowInitiativeView(BaseShowInitiativeView):
    def get(self, request, initiative_pk):
        lang = request.GET.get('lang', '')
        language_codes = lang.split(',')
        if language_codes == ['']:
            language_codes = []

        initiative = get_object_or_404(Initiative, pk=initiative_pk)
        lang_obj = initiative.first_of_specified_languages(language_codes)
        version = lang_obj.last_version if lang_obj else None

        return self.do_get(request, version, bool(version), lang, lang_obj)


class ShowInitiativeVersionView(BaseShowInitiativeView):
    def get(self, request, version_pk):
        version = get_object_or_404(InitiativeVersion, pk=version_pk)
        lang_obj = version.initiative_language

        return self.do_get(request, version, version == lang_obj.last_version, None, lang_obj)


class ListInitiativeView(View):
    def get(self, request):
        lang = request.GET.get('lang', '')
        language_codes = lang.split(',')
        if language_codes == ['']:
            language_codes = []
        cat = request.GET.get('cat', '')
        categories = cat.split(',')
        if categories == ['']:
            categories = []
        try:
            categories = [int(c) for c in categories]
        except ValueError:
            return HttpResponse(_("Invalid parameter 'cat'."), status=400)

        if language_codes == []:
            lang_code = get_language_from_request(request, check_path=True)
            language_codes = [lang_code]

        lst = Initiative.objects.filter(languages__language__in=language_codes)
        if categories:
            lst = lst.filter(categories__pk__in=categories)
        lst = lst.distinct('pk').order_by('-pk')

        paginator = Paginator(lst, 25)
        page = request.GET.get('page')
        initiatives = paginator.get_page(page)

        # Without list(), version|length in template does not work
        versions = list(i.version_in_specified_languages(language_codes) for i in initiatives)

        all_categories = InitiativeCategory.objects.all()

        # Remove duplicate content
        # nofollow = not InitiativeLanguage.objects.filter(language__in=language_codes).exists()

        return render(request, 'initiative/list.html',
                      {'is_initiatives_list': True,
                       'versions': versions,
                       'paginator': paginator,
                       'page_obj': initiatives,
                       'categories': categories,
                       'all_categories': all_categories})


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
        initiative = form.save()
        return redirect(reverse('initiative:view', initiative.pk) + '?lang=' + form.fields['language'])


class EditInitiativeView(LoginRequiredMixin, View):
    def get(self, request, initiative_pk):
        initiative = get_object_or_404(Initiative, pk=initiative_pk)
        version = initiative.last_version  # FIXME: language
        if request.GET.get('translate'):
            version.language = ''
            version.title = ""
            version.problem = ""
            version.solution = ""
            version.outcome = ""
        form = InitiativeForm(instance=version)
        return render(request, 'initiative/initiative-form.html', {'form': form})

    def post(self, request):
        form = InitiativeForm(request.POST)
        form.fields['editor'] = request.user
        initiative = form.save()
        return redirect(reverse('initiative:view', initiative.pk) + '?lang=' + form.fields['language'])


class AjaxVoteView(View):
    def post(self, request, pool, against, reclaim, initiative_pk):
        initiative = get_object_or_404(Initiative, pk=initiative_pk)
        vote_form = VoteForm(request, initiative)

        if pool == 'main':
            vote_form.fields['vote'].vote(request, vote_form.initial['vote'], against, reclaim)
        elif pool == 'spam':
            vote_form.fields['vote_being_spam'].vote(request, vote_form.initial['vote_being_spam'], against, reclaim)
        else:
            return HttpResponse("Bad voting pool.", status=400)  # Don't translate.

        return HttpResponse('ok')
