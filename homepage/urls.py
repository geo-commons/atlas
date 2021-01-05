from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from homepage import views

app_name = 'homepage'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('savedataset', views.SavedDatasetView.as_view(), name='savedataset'),
    path('handleiding/', views.HandleidingView.as_view(), name='handleiding'),
    path('downloads/', views.DownloadsView.as_view(), name='downloads'),
    path('downloads/<int:pk>/<str:type_>', views.save_dataset_view, name='save_dataset_view'),
    path('search_wfs', views.search_wfs, name='search_wfs'),
    path('autocomplete_search', views.autocomplete_search, name='autocomplete_search'),
    path('v3/help', views.v3_help, name='v3_help'),
    path('v3/login', auth_views.LoginView.as_view(template_name='v3/login.html'), name='v3_login'),
    path('v3/logout', auth_views.LogoutView.as_view(template_name='v3/logout.html'), name='v3_logout'),
    re_path('v3/', views.v3, name='v3'),
    re_path('embed/', views.embed, name='embed'),
]
