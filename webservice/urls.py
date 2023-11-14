from rest_framework import routers
from . import viewsets

api_router = routers.DefaultRouter()
api_router.register(r'maps', viewsets.MapViewSet, basename='maps')
api_router.register(r'sources', viewsets.SourceViewSet, basename='sources')
api_router.register(r'layers', viewsets.LayerViewSet, basename='layers')
api_router.register(r'drawings', viewsets.DrawingViewSet, basename='drawings')
api_router.register(r'categories', viewsets.CategoriesViewSet, basename='categories')
api_router.register(r'users', viewsets.UsersViewSet, basename='users')
api_router.register(r'groups', viewsets.GroupsViewSet, basename='groups')