from django.urls import re_path, path
from . import views
from portal import views as portal_views

app_name = 'tables'

urlpatterns = [
    path('', portal_views.index, name='tables_root'),
    re_path(r'^.+', views.index, name='tables_index'),
]
