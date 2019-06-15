from django.urls import path, re_path

import user.views

app_name = 'user'
urlpatterns = [
    path('register', user.views.Register.as_view(), name='register'),
    path('account', user.views.Account.as_view(), name='account'),
    re_path(r'profile/(\d+)', user.views.ViewProfile.as_view(), name='profile'),
]
