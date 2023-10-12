from rest_framework import viewsets, permissions, mixins

from .models import Category, Drawing, Map, Source, Layer
from .serializers import CategorySerializer, LayerCreateUpdateSerializer, LayerListSerializer, MapSerializer, SourceSerializer, LayerSerializer


class MapViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    search_fields = []
    filterset_fields = []


class SourceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    search_fields = []
    filterset_fields = []


class LayerViewSet(viewsets.ModelViewSet):
    serializer_class = LayerSerializer

    search_fields = []
    filterset_fields = ['layer_source']

    def get_serializer_class(self):
        if self.action == 'list':
            return LayerListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return LayerCreateUpdateSerializer

        return LayerSerializer

    def get_queryset(self):
        return Layer.authorized.for_request(self.request).prefetch_related('atlas_groups')


class DrawingViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Drawing.objects.all()
    
class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    search_fields = []
    filterset_fields = []