from rest_framework import viewsets, permissions, mixins

from .models import Drawing, Map, Source, Layer
from .serializers import DrawingSerializer, MapSerializer, SourceSerializer, LayerSerializer


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
    permission_classes = [permissions.IsAdminUser]
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    search_fields = []
    filterset_fields = []


class DrawingViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
