from rest_framework import routers
from . import viewsets


tables_api_router = routers.DefaultRouter()

tables_api_router.register(r'tables', viewsets.TableViewSet, basename='tables')