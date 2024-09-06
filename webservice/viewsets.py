from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.exceptions import NotFound

from tables.models import Table
from tables.serializers import TableSerializer
from user_management.models import AtlasGroup, AtlasUser
from webservice.mixins import DataExportImportMixin

from .models import Category, Drawing, Map, Source, Layer, Dataset, Theme, Viewer
from .serializers import CategorySerializer, DrawingSerializer, GroupSerializer, LayerCreateUpdateSerializer, \
    LayerListSerializer, MapSerializer, SourceSerializer, LayerSerializer, UserSerializer, DatasetSerializer, \
    ThemeSerializer, ThemePatchOrCreateSerializer, DatasetPatchOrCreateSerializer, ViewerSerializer


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


class DatasetViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Dataset.objects.all().prefetch_related('layers')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['themes']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'create']:
            return DatasetPatchOrCreateSerializer
        return DatasetSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        lookup_field_value = self.kwargs.get('pk')

        # Check if the lookup value is numeric (for id) or not (for slug)
        if lookup_field_value.isdigit():
            # Try to retrieve by primary key (id)
            obj = queryset.filter(pk=lookup_field_value).first()
        else:
            # If not numeric, try to retrieve by slug
            obj = queryset.filter(slug=lookup_field_value).first()

        if obj is None:
            raise NotFound(f"No Dataset matches the given query: {lookup_field_value}")

        return obj


class ThemeViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'create']:
            return ThemePatchOrCreateSerializer
        return ThemeSerializer


class ViewerViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Viewer.objects.all()
    serializer_class = ViewerSerializer

class TableViewSet(DataExportImportMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Table.objects.all()
    serializer_class = TableSerializer
