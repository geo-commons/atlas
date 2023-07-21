from rest_framework import viewsets, permissions as rest_framework_permissions

from .models import Map, Layer
from .serializers import MapSerializer, LayerSerializer
from .permissions import IsAdminUser, IsAdminOrReadOnly
from utils.tools import is_ctrix


class MapViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    search_fields = []
    filterset_fields = []


class LayerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = LayerSerializer

    search_fields = []
    filterset_fields = ['layer_source']

    def get_queryset(self):
        return Layer.authorized.user_or_group(
            self.request.user,
            is_ctrix(self.request)
        )
