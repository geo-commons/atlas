import copy

from constance import config
from constance import settings as constance_settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authz.models import Log
from tables.models import Table
from tables.serializers import TableSerializer
from user_management.models import AtlasGroup, AtlasUser
from webservice.exceptions import ProtectedDeleteError
from webservice.mixins import DataExportImportMixin, DuplicateMixin, DeleteMixin, FileUploadMixin
from webservice.util import get_settings, process_value
from .filters import MultipleFieldsFilter
from .models import Category, Drawing, Source, Layer, Viewer, Map, MapLayer, MapCategory, Metadataset, TopicCategory, \
    RoleType, UpdateMethodType, AuthorizationLevelType, StatusType, AccessConstraintsType, OtherConstraintsType
from .serializers import CategorySerializer, DrawingSerializer, GroupSerializer, LayerCreateUpdateSerializer, \
    LayerListSerializer, MapSerializer, SourceSerializer, LayerSerializer, UserSerializer, \
    LogSerializer, ViewerSerializer, UserCreateUpdateSerializer, MetadatasetSerializer, DeleteSettingsSerializer, \
    MetadatasetPublicSerializer


class MapViewSet(DataExportImportMixin, FileUploadMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    serializer_class = MapSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, MultipleFieldsFilter, OrderingFilter]
    multiple_lookup_fields = ['published', 'show_in_overview', 'is_main']

    search_fields = ['title', 'description', 'keywords', 'about']

    def get_queryset(self):
        return Map.authorized.for_request(self.request)

    def destroy(self, request, *args, **kwargs):
        map_instance = self.get_object()
        if map_instance.is_main:
            raise ValidationError({'detail': 'De hoofdkaart kan niet worden verwijderd.'})

        return super().destroy(request, *args, **kwargs)

    def prepare_duplicate(self, duplicate):
        """
        Prepare a duplicated map and ensure it cannot become the main map.
        """
        duplicate = super().prepare_duplicate(duplicate)
        duplicate.is_main = False
        duplicate.features = copy.deepcopy(duplicate.features)
        duplicate.settings = copy.deepcopy(duplicate.settings)
        return duplicate

    def get_many_to_many_values(self, _obj):
        """
        Skip generic many-to-many copying because map layers use through models.
        """
        return {}

    def after_duplicate(self, obj, duplicate):
        """
        Copy map-specific category and layer relations after saving the map.
        """
        category_mapping = self._duplicate_map_categories(obj, duplicate)
        self._duplicate_map_layers(obj, duplicate, category_mapping)

    def _duplicate_map_categories(self, obj, duplicate):
        """
        Copy map categories and return old-to-new category mappings.
        """
        category_mapping = {}
        original_categories = MapCategory.objects.filter(map=obj).select_related('category')
        for original_category in original_categories:
            duplicated_category = MapCategory.objects.create(
                map=duplicate,
                category=original_category.category,
                ordering=original_category.ordering,
            )
            category_mapping[original_category.id] = duplicated_category

        return category_mapping

    def _duplicate_map_layers(self, obj, duplicate, category_mapping):
        """
        Copy map layers and link them to duplicated map categories.
        """
        original_layers = MapLayer.objects.filter(map=obj).select_related('layer', 'map_category')
        for original_layer in original_layers:
            MapLayer.objects.create(
                map=duplicate,
                layer=original_layer.layer,
                map_category=category_mapping.get(original_layer.map_category_id),
                settings=copy.deepcopy(original_layer.settings),
                ordering=original_layer.ordering,
            )

    @action(detail=False, methods=['post'], url_path='delete', permission_classes=[permissions.IsAdminUser])
    def data_delete(self, request):
        serializer = DeleteSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids_to_delete = serializer.validated_data.get('ids', [])
        protected_ids = list(Map.objects.filter(id__in=ids_to_delete, is_main=True).values_list('id', flat=True))
        if protected_ids:
            raise ValidationError({'detail': 'De hoofdkaart kan niet worden verwijderd.', 'ids': protected_ids})

        Map.objects.filter(id__in=ids_to_delete).delete()

        return Response({
            'message': 'Successfully deleted objects',
        })


class SourceViewSet(DataExportImportMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]

    search_fields = ['title']


class LayerViewSet(DataExportImportMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    serializer_class = LayerSerializer

    search_fields = ['title']

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, MultipleFieldsFilter]
    multiple_lookup_fields = ['layer_source', 'layer_type']

    def get_serializer_class(self):
        if self.action == 'list':
            return LayerListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return LayerCreateUpdateSerializer

        return LayerSerializer

    def get_queryset(self):
        return Layer.authorized.for_request(self.request).prefetch_related('atlas_groups', 'related_tables').select_related(
            'layer_source',
            'layer_type',
            'layer_type__parent',
            'metadataset',
        )


class DrawingViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer


class CategoriesViewSet(DataExportImportMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.select_related('parent').all()
    serializer_class = CategorySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]

    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category.children.exists():
            raise ProtectedDeleteError(
                'Het is niet mogelijk om een hoofdcategorie met subcategorieën te verwijderen.'
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='delete', permission_classes=[permissions.IsAdminUser])
    def data_delete(self, request):
        serializer = DeleteSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids_to_delete = serializer.validated_data.get('ids', [])
        has_parent_categories = Category.objects.filter(
            id__in=ids_to_delete,
            children__isnull=False,
        ).exists()
        
        if has_parent_categories:
            raise ProtectedDeleteError(
                'Het is niet mogelijk om een hoofdcategorie met subcategorieën te verwijderen.'
            )

        Category.objects.filter(id__in=ids_to_delete).delete()

        return Response({
            'message': 'Successfully deleted objects',
        })


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = AtlasUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, MultipleFieldsFilter, OrderingFilter]

    search_fields = ['username', 'email', 'first_name', 'last_name', 'name']
    multiple_lookup_fields = ['atlas_groups']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer

        return UserSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = AtlasGroup.objects.all().order_by('name')
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]

    search_fields = ['name']


class MetadatasetViewSet(viewsets.ModelViewSet, DataExportImportMixin, DuplicateMixin, DeleteMixin):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']
    serializer_class = MetadatasetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, MultipleFieldsFilter, OrderingFilter]
    multiple_lookup_fields = ['topic_category', 'status', 'show_in_overview']
    search_fields = ['title', 'abstract', 'keyword']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Return different serializers based on whether the user is authenticated or not.
        Authenticated users get all fields including internal email addresses.
        Anonymous users get only public fields.
        """
        if self.request.user.is_authenticated:
            return MetadatasetSerializer
        else:
            return MetadatasetPublicSerializer

    def get_queryset(self):
        return Metadataset.authorized.for_request(self.request).prefetch_related(
            Prefetch(
                'layers', 
                queryset=
                    Layer.authorized.for_request(self.request)
                    .order_by('title')
                )
            )

    def get_object(self):
        queryset = self.get_queryset()
        lookup_field_value = self.kwargs.get('pk')

        # first check if the lookup field is a slug
        obj = queryset.filter(slug=lookup_field_value).first()

        # if not, check if the lookup field is a primary key
        if obj is None and lookup_field_value.isdigit():
            obj = queryset.filter(pk=lookup_field_value).first()

        # if not, raise an error
        if obj is None:
            raise NotFound(f"No Metadataset matches the given query: {lookup_field_value}")

        return obj


class ViewerViewSet(DataExportImportMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser]
    queryset = Viewer.objects.all()
    serializer_class = ViewerSerializer

    search_fields = ['label']

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]


class TableViewSet(DataExportImportMixin, DeleteMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = TableSerializer

    search_fields = ['title', 'description']

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        return Table.authorized.for_request(self.request)


class LogViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [permissions.IsAdminUser]
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    search_fields = ['username']

    filter_backends = [SearchFilter, DjangoFilterBackend, MultipleFieldsFilter, OrderingFilter]
    multiple_lookup_fields = ['username', 'source', 'resource']

    @action(detail=False, methods=['get'], url_path='unique-fields')
    def unique_fields(self, request):
        unique_usernames = Log.objects.order_by('username').values_list('username', flat=True).distinct()
        unique_sources = Log.objects.order_by('source').values_list('source', flat=True).distinct()
        unique_resources = Log.objects.order_by('resource').values_list('resource', flat=True).distinct()

        data = {
            "usernames": list(unique_usernames),
            "sources": list(unique_sources),
            "resources": list(unique_resources)
        }

        return Response(data)


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
                        # file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
                        file_path = uploaded_file.name
                        # Save the file
                        path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
                        # Save the file path in the Constance setting (key is the field name)
                        setattr(config, key, path)
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


def enum_to_dict_list(enum_cls):
    return [{"value": member.value, "label": member.label} for member in enum_cls]


class BaseEnumViewSet(viewsets.ViewSet):
    """List-only endpoint for TextChoices enums."""
    permission_classes = [AllowAny]
    pagination_class = None
    enum_cls = None

    def list(self, request):
        return Response(enum_to_dict_list(self.enum_cls))


class TopicCategoryViewSet(BaseEnumViewSet):
    enum_cls = TopicCategory


class RoleTypeViewSet(BaseEnumViewSet):
    enum_cls = RoleType


class UpdateMethodTypeViewSet(BaseEnumViewSet):
    enum_cls = UpdateMethodType


class AuthorizationLevelTypeViewSet(BaseEnumViewSet):
    enum_cls = AuthorizationLevelType


class StatusTypeViewSet(BaseEnumViewSet):
    enum_cls = StatusType


class AccessConstraintsTypeViewSet(BaseEnumViewSet):
    enum_cls = AccessConstraintsType


class OtherConstraintsTypeViewSet(BaseEnumViewSet):
    enum_cls = OtherConstraintsType
