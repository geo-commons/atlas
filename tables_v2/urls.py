from rest_framework import routers
from . import viewsets


tables_api_router = routers.DefaultRouter()

# TODO: refactor to use prefix 'tables' instead of 'tables_v2' and basename 'tables' instead of 'tables_v2'
tables_api_router.register(r'tables-v2', viewsets.TableTempViewSet, basename='tables-v2')