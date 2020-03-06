from django.urls import path

from homepage.views import (DownloadsView, HomePageView, HandleidingView,
                            autocomplete_search,
                            search_wfs, SavedDatasetView,
                            save_dataset_view)

app_name = 'homepage'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('savedataset', SavedDatasetView.as_view(), name='savedataset'),
    path('handleiding/', HandleidingView.as_view(), name='handleiding'),
    path('downloads/', DownloadsView.as_view(), name='downloads'),
    path('downloads/<int:pk>/<str:type_>', save_dataset_view,
         name='save_dataset_view'),
    path('search_wfs', search_wfs, name='search_wfs'),
    path('autocomplete_search', autocomplete_search,
         name='autocomplete_search'),
]
