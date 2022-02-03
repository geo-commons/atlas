from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from rest_framework import routers
from homepage import views
from webservice.views import MapDetailView
from webservice import viewsets

app_name = 'homepage'

urlpatterns = [
    path('v2/', views.HomePageView.as_view(), name='homepage'),
    path('v2/savedataset', views.SavedDatasetView.as_view(), name='savedataset'),
    path('v2/handleiding/', views.HandleidingView.as_view(), name='handleiding'),
    path('v2/downloads/', views.DownloadsView.as_view(), name='downloads'),
    path('v2/downloads/<int:pk>/<str:type_>', views.save_dataset_view, name='save_dataset_view'),
    path('v2/search_wfs', views.search_wfs, name='search_wfs'),
    path('v2/autocomplete_search', views.autocomplete_search, name='autocomplete_search'),
    path('v2/<slug:slug>', MapDetailView.as_view(), name='map-detail'),
]

router = routers.DefaultRouter()
router.register(r'maps', viewsets.MapViewSet, basename='maps')

urlpatterns += [
    path('help', views.v3_help, name='v3_help'),
    path('disclaimer', views.v3_disclaimer, name='v3_disclaimer'),
    path('login', auth_views.LoginView.as_view(template_name='v3/login.html'), name='v3_login'),
    path('login/failure', views.v3_login_failure, name='v3_login_failure'),
    path('logout', auth_views.LogoutView.as_view(template_name='v3/logout.html'), name='v3_logout'),
    path('admin2/', views.v3_admin, name='v3_admin'),
    path('api/v1/token', views.v3_token, name='v3_token'),
    path('api/v1/', include(router.urls)),
    re_path('embed', views.embed, name='embed'),
    re_path(r'((?P<theme_slug>[a-z0-9\-]+)?)', views.v3, name='v3'),
]
