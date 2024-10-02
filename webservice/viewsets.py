from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.viewsets import ViewSet
from constance import config
from constance import settings as constance_settings
from rest_framework.exceptions import NotFound

from authz.models import Log
from tables.models import Table
from tables.serializers import TableSerializer
from user_management.models import AtlasGroup, AtlasUser
from webservice.mixins import DataExportImportMixin
from webservice.util import get_settings, process_value

from .models import Category, Drawing, Map, Source, Layer, Dataset, Theme, Viewer
from .serializers import CategorySerializer, DrawingSerializer, GroupSerializer, LayerCreateUpdateSerializer, \
    LayerListSerializer, MapSerializer, SourceSerializer, LayerSerializer, UserSerializer, DatasetSerializer, \
    ThemeSerializer, ThemePatchOrCreateSerializer, DatasetPatchOrCreateSerializer, LogSerializer, ViewerSerializer

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

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

    search_fields = ['title']
    filterset_fields = ['layer_source']

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

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
    serializer_class = DatasetSerializer

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


class LogViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete']
    permission_classes = [permissions.IsAdminUser]
    serializer_class = LogSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Log.objects.all().order_by('-id')[:5000]

        return Log.objects.all()


class ConfigurationViewSet(ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def setting(self, request, allow_settings):

        if request.method != 'GET':
            # change all allow setting items in allow_settings
            for key, value in request.data.items():
                if key in allow_settings:
                    # Check if current field is an image field by checking if the key has a corresponding file.
                    if (key in request.FILES):
                        uploaded_file = request.FILES[key]
                        # Define the path to save the file
                        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
                        # Save the file
                        path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                        # Save the file path in the Constance setting
                        setattr(config, 'ORGANIZATION_LOGO', path)
                    else:
                        setattr(config, key, process_value(value))

        return Response(data=get_settings(allow_settings))


    def create(self, request):
        """
        Update with POST: {'Key': new_value}
        """
        settings = constance_settings.CONFIG.items()
        allow_settings = [key for key, options in settings]

        return self.setting(request, allow_settings)

    def list(self, request):
        """
        Get all setting item
        """
        settings = constance_settings.CONFIG.items()
        allow_settings = [key for key, options in settings]

        return self.setting(request, allow_settings)