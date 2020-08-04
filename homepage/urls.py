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
    re_path('embed/', views.embed, name='embed'),
]
