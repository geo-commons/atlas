from django.urls import re_path
from . import views

app_name = 'portal'

urlpatterns = [
    re_path('', views.index, name='portal_index'),
]
