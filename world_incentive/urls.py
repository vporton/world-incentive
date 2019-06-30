"""world_incentive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.contrib.sitemaps import views as sitemap_views

import core.urls
import initiative.urls
import main.views
import user.urls
from core.views import InitiativeSitemap, InitiativeVersionSitemap, UserSitemap, StaticViewSitemap

sitemaps = {'static': StaticViewSitemap,
            'initiatives': InitiativeSitemap,
            'initiative-versions': InitiativeVersionSitemap,
            'users': UserSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('django.contrib.auth.urls'))),
    path('admin/defender/', include('defender.urls')),
    path('', main.views.MainPage.as_view(), name='mainpage'),
    path('core/', include(core.urls)),
    path('user/', include(user.urls)),
    path('initiative/', include(initiative.urls)),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
