from django.urls import path, re_path

from initiative import views

app_name = 'initiative'
urlpatterns = [
    path('create-prompt', views.CreateInitiativePromptView.as_view(), name='create-prompt'),
    path('create', views.CreateInitiativeView.as_view(), name='create'),
]
