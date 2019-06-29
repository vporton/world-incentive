from django.urls import path, re_path

from initiative import views

app_name = 'initiative'
urlpatterns = [
    path('view/<int:initiative_pk>', views.ShowInitiativeView.as_view(), name='view'),
    path('view-old/<int:version_pk>', views.ShowInitiativeVersionView.as_view(), name='view-old'),
    path('list', views.ListInitiativeView.as_view(), name='list'),
    path('create-prompt', views.CreateInitiativePromptView.as_view(), name='create-prompt'),
    path('create', views.CreateInitiativeView.as_view(), name='create'),
    path('edit/<int:initiative_pk>/<language>', views.EditInitiativeView.as_view(), name='edit'),
    path('translate/<int:initiative_pk>', views.TranslateInitiativeView.as_view(), name='translate'),
    path('ajax-vote/<str:pool>:<int:against>:<int:reclaim>/<int:initiative_pk>', views.AjaxVoteView.as_view(), name='vote')
]
