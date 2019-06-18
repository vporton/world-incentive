from django.utils.translation import get_language_from_request

from core.forms import LanguageChoiceForm


def language_choice_form_context_processor(request):
    language = get_language_from_request(request, check_path=True)
    return {
        'language_choice_form': LanguageChoiceForm(initial={'language': language}),
    }