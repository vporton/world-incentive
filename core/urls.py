from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    path('cities-ajax/<int:level>/<int:parent_pk>', views.CitiesAjaxView.as_view()),
]
