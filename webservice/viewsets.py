from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, filters

from user_management.models import AtlasGroup, AtlasUser
from webservice.mixins import DataExportImportMixin

from .models import Category, Drawing, Map, Source, Layer, Dataset, Theme
from .serializers import CategorySerializer, DrawingSerializer, GroupSerializer, LayerCreateUpdateSerializer, \
    LayerListSerializer, MapSerializer, SourceSerializer, LayerSerializer, UserSerializer, DatasetSerializer, \
    ThemeSerializer, ThemePatchOrCreateSerializer, DatasetPatchOrCreateSerializer


class MapViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    search_fields = []
    filterset_fields = []


class SourceViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    search_fields = []
    filterset_fields = []


class LayerViewSet(DataExportImportMixin, viewsets.ModelViewSet):
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
    serializer_class = DrawingSerializer


class CategoriesViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    search_fields = []
    filterset_fields = []


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = AtlasUser.objects.all()
    serializer_class = UserSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = AtlasGroup.objects.all()
    serializer_class = GroupSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Dataset.objects.all().prefetch_related('layers')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['themes']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'create']:
            return DatasetPatchOrCreateSerializer
        return DatasetSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Theme.objects.all()

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'create']:
            return ThemePatchOrCreateSerializer
        return ThemeSerializer
