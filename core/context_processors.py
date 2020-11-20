from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.translation import get_language_from_request

from core.forms import LanguageChoiceForm
from user.models import User


def settings_context_processor(request):
    return {
        'settings': settings,
    }


def language_choice_form_context_processor(request):
    language = get_language_from_request(request, check_path=True)
    user_languages = [language] if request.user.is_anonymous \
        else request.user.languages.all().values_list('language', flat=True)
    get_token(request)  # to turn on CSRF
    return {
        'lang': language,
        'user_languages': ','.join(user_languages),
        'language_choice_form': LanguageChoiceForm(initial={'language': language}),
    }