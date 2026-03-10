from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.index, name='portal_index'),
    path('maps/', views.index, name='portal_maps'),
    path('metadatasets/', views.index, name='portal_metadatasets'),
    path('metadatasets/<slug:slug>/', views.index, name='portal_metadataset_detail'),
    path('tables/', views.index, name='portal_tables'),
    path('tables/<slug:slug>/', views.index, name='portal_table_detail'),
    path('search/', views.index, name='portal_search'),
]
