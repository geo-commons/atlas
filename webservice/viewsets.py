from rest_framework import viewsets, permissions

from .models import Map
from .serializers import MapSerializer

class MapViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    search_fields = []
    filterset_fields = []
