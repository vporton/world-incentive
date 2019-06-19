from django.urls import path, re_path

from initiative import views

app_name = 'initiative'
urlpatterns = [
    path('view/<int:initiative_pk>', views.ShowInitiativeView.as_view(), name='view'),
    path('create-prompt', views.CreateInitiativePromptView.as_view(), name='create-prompt'),
    path('create', views.CreateInitiativeView.as_view(), name='create'),
]
