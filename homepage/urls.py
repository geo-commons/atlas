from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from homepage import views, viewclasses
from webservice import views as webservice_views, urls
from tables_v2 import urls as tables_urls

app_name = 'homepage'

urlpatterns = [
    path('disclaimer', views.v3_disclaimer, name='v3_disclaimer'),
    path('login', viewclasses.LoginView.as_view(
        template_name='v3/login.html'), name='v3_login'),
    path('login/failure', views.v3_login_failure, name='v3_login_failure'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='v3/logout.html'), name='v3_logout'),
    path('admin/', views.v3_admin, name='v3_admin'),
    path('api/v1/token', webservice_views.v3_token, name='v3_token'),
    path('api/v1/', include(urls.api_router.urls)),
    path('api/v1/', include(tables_urls.tables_api_router.urls)),
    path('convert/<str:output_format>',
         webservice_views.v3_convert, name='v3_convert'),
    # This embed route is retained for backward compatibility with legacy /atlas/embed/* URLs.
    # New embedded maps should use /atlas/maps/{slug} or /atlas/.
    re_path(r'embed/.*$', views.embed, name='embed'),
    re_path(r'maps\/((?P<slug>[a-z0-9\-]+)?)', views.v3_map, name='v3_map'),
    re_path(r'((?P<theme_slug>[a-z0-9\-]+)?)', views.v3, name='v3'),
]
