"""atlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.conf import settings
from . import admin as custom_admin

admin.site.site_header = 'Atlas beheer'
admin.site.site_title = 'Atlas beheer'
admin.site.site_url = '/atlas'

urlpatterns = [
    path('atlas/admin/', admin.site.urls),
    path('catalog/admin/', custom_admin.site.urls),
]

if settings.AUTHENTICATION_ENABLE_CREDENTIALS:
    urlpatterns += [
        path('atlas/accounts/', include('django.contrib.auth.urls'))
    ]

if settings.AUTHENTICATION_ENABLE_OIDC:
    urlpatterns += [
        path('atlas/oidc/', include('mozilla_django_oidc.urls'))
    ]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^atlas/media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

urlpatterns += [
    path('atlas/', include('homepage.urls'), name='homepage'),
    path('catalog/', include('catalog.urls'), name='catalog'),
    path('', RedirectView.as_view(url='/atlas/'))
]
