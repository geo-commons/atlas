from django.urls import path
from . import views

app_name = 'brp'

urlpatterns = [
    path('', views.index, name='index'),
]
