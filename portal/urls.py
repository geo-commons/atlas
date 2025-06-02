from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.index, name='portal_index'),
]
