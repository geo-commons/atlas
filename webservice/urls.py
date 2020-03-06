from django.urls import path

from .views import AtlasThemeDetailView

app_name = 'webservice'

urlpatterns = [
    path('<slug:slug>', AtlasThemeDetailView.as_view(),
         name='atlastheme-detail'),
]
