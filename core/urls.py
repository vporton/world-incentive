from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    path('set-language', views.SetLanguageView.as_view()),
    path('cities-ajax/<int:level>/<int:parent_pk>', views.CitiesAjaxView.as_view()),
]
