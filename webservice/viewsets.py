from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Map, Layer
from .serializers import MapSerializer, LayerSerializer, UserSerializer


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


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response([])

        return Response()

    def retrieve(self, request, pk=None):
        if pk != 'me':
            raise NotFound(detail='Could not find this user', code=404)

        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        return Response()
