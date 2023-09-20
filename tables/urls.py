from django.urls import re_path
from . import views

app_name = 'tables'

urlpatterns = [
    re_path('', views.index, name='tables_index'),
]
