from rest_framework import viewsets, permissions

from .models import AtlasTheme
from .serializers import AtlasThemeSerializer

class AtlasThemeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = AtlasTheme.objects.all()
    serializer_class = AtlasThemeSerializer

    search_fields = []
    filterset_fields = []
