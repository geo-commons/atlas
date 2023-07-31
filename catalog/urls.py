from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('datasets', views.DatasetListView.as_view(), name='datasets'),
    path('datasets/<slug:slug>',
         views.DatasetDetailView.as_view(), name='datasets-detail')
]
