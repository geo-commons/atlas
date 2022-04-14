from rest_framework import viewsets, permissions

from .models import Map, Layer
from .serializers import MapSerializer, LayerSerializer

class MapViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    search_fields = []
    filterset_fields = []


class LayerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    search_fields = []
    filterset_fields = []
