from django.urls import re_path, path

from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.index, name='tables_root'),
    re_path(r'^.+', views.index, name='tables_index'),
]
