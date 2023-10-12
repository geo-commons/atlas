from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from rest_framework import routers
from homepage import views, viewclasses
from webservice import viewsets, views as webservice_views

app_name = 'homepage'

api_router = routers.DefaultRouter()
api_router.register(r'maps', viewsets.MapViewSet, basename='maps')
api_router.register(r'sources', viewsets.SourceViewSet, basename='sources')
api_router.register(r'layers', viewsets.LayerViewSet, basename='layers')
api_router.register(r'drawings', viewsets.DrawingViewSet, basename='drawings')
api_router.register(r'categories', viewsets.CategoriesViewSet, basename='categories')

urlpatterns = [
    path('help', views.v3_help, name='v3_help'),
    path('disclaimer', views.v3_disclaimer, name='v3_disclaimer'),
    path('login', viewclasses.LoginView.as_view(
        template_name='v3/login.html'), name='v3_login'),
    path('login/failure', views.v3_login_failure, name='v3_login_failure'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='v3/logout.html'), name='v3_logout'),
    path('admin2/', views.v3_admin, name='v3_admin'),
    path('api/v1/token', webservice_views.v3_token, name='v3_token'),
    path('api/v1/authorize', webservice_views.v3_authorize, name='v3_authorize'),
    path('api/v1/', include(api_router.urls)),
    path('convert/<str:output_format>',
         webservice_views.v3_convert, name='v3_convert'),
    re_path('embed', views.embed, name='embed'),
    re_path(r'maps\/((?P<slug>[a-z0-9\-]+)?)', views.v3_map, name='v3_map'),
    re_path(r'((?P<theme_slug>[a-z0-9\-]+)?)', views.v3, name='v3'),
]
