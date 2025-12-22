from django.utils.text import slugify
from rest_framework import serializers

from authz.lib import can_request_access_layer
from authz.models import Log
from user_management.models import AtlasGroup, AtlasUser
from .models import Category, Drawing, LinkedData, Map, MapLayer, Source, Layer, Template, Dataset, Theme, Viewer, \
    Metadataset
from .util import safe_float_or_null


class MapLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLayer
        fields = ['layer', 'settings']


class MapSerializer(serializers.ModelSerializer):
    layers = MapLayerSerializer(many=True, source='map_layers')

    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers', 'thumbnail', 'description', 'published',
                  'show_in_overview', 'about', 'about_title']

    def create(self, validated_data):
        try:
            map_layers = validated_data.pop('map_layers')
        except KeyError:
            map_layers = None

        created_map = Map.objects.create(**validated_data)

        if map_layers is not None:
            for map_layer in map_layers:
                created_map.map_layers.create(
                    layer=map_layer.get('layer'),
                    settings=map_layer.get('settings')
                )

        return created_map

    def update(self, instance, validated_data):
        try:
            map_layers = validated_data.pop('map_layers')
        except KeyError:
            map_layers = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if map_layers is not None:
            map_layers_to_create = []
            for map_layer in map_layers:
                map_layers_to_create.append(MapLayer(
                    layer=map_layer.get('layer'),
                    settings=map_layer.get('settings')
                ))

            instance.map_layers.all().delete()
            instance.map_layers.set(map_layers_to_create, bulk=False)

        return instance


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title', 'slug', 'url', 'authenticate', 'source_type', 'atlas_groups', 'login_required']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'ordering']


class LinkedDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='layer_name')
    display_properties = serializers.ListField(
        child=serializers.CharField(), required=False)
    headers = serializers.ListField(
        child=serializers.CharField(), required=False)
    detail_view_fields = serializers.ListField(
        child=serializers.CharField(), required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['display_properties'] = instance.popup_attributes.split(
            '\r\n') if instance.popup_attributes else []
        ret['headers'] = instance.headers.split(
            '\r\n') if instance.headers else []
        ret['detail_view_fields'] = instance.detail_view_fields.split(
            '\r\n') if instance.detail_view_fields else []
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['popup_attributes'] = '\r\n'.join(
            data.get('display_properties', []))
        ret['headers'] = '\r\n'.join(data.get('headers', []))
        ret['detail_view_fields'] = '\r\n'.join(data.get('detail_view_fields', []))
        return ret

    class Meta:
        model = LinkedData
        fields = ['id', 'source', 'title', 'name', 'url', 'source_key', 'target_key',
                  'display_properties', 'headers', 'use_detail_view', 'detail_view_fields']


class TemplateSerializer(serializers.ModelSerializer):
    source_id = serializers.PrimaryKeyRelatedField(
        source='source', queryset=Source.objects.all())
    source = SourceSerializer(read_only=True)
    fields = serializers.ListField(
        child=serializers.CharField(), required=False)
    headers = serializers.ListField(
        child=serializers.CharField(), required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'source' not in ret:
            ret['source'] = SourceSerializer(instance.source).data
        ret['fields'] = instance.fields.split(
            '\r\n') if instance.fields else []
        ret['headers'] = instance.headers.split(
            '\r\n') if instance.headers else []
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        source_id = data.get('source_id')
        if source_id:
            data['source'] = Source.objects.get(pk=source_id)
        ret['fields'] = '\r\n'.join(data.get('fields', []))
        ret['headers'] = '\r\n'.join(data.get('headers', []))
        return ret

    class Meta:
        model = Template
        fields = ['id', 'title', 'source', 'endpoint', 'method', 'list',
                  'headers', 'fields', 'template', 'ordering', 'source_id']


class MetadataSerializerField(serializers.Field):

    def to_representation(self, value):
        return {
            'name': value.meta_name,
            'description': value.meta_description,
            'organization': value.meta_org,
            'updated': value.meta_updated,
            'link': value.meta_link,
            'lineage': value.meta_lineage,
            'contact': value.meta_contact
        }

    def to_internal_value(self, data):
        return {
            'meta_name': data['name'],
            'meta_description': data['description'],
            'meta_org': data['organization'],
            'meta_updated': data['updated'],
            'meta_lineage': data['lineage'],
            'meta_contact': data['contact'],
            'meta_link': data['link'],
        }


class MetadatasetPublicSerializer(serializers.ModelSerializer):
    """Serializer for external/public API calls - excludes internal email addresses and sensitive fields"""

    class Meta:
        model = Metadataset
        fields = [
            'id',
            'title',
            'slug',
            'abstract',
            'topic_category',
            'keyword',
            'statement',
            'source_origin',
            'source_organization',
            'source_name_public',
            'source_email_public',
            'source_email_person_responsible',
            'source_role_person_responsible',
            'update_frequency',
            'last_updated',
            'status',
            'show_in_overview',
            'access_constraints',
            'other_constraints',
            'usage_constraints',
            'meta_organization',
            'meta_email_person_responsible',
            'meta_role_person_responsible',
        ]


class MetadatasetSerializer(serializers.ModelSerializer):
    """Serializer for internal API calls - includes all fields including internal email addresses"""

    class Meta:
        model = Metadataset
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'abstract',
            'topic_category',
            'keyword',
            'statement',
            'source_origin',
            'source_location',
            'source_name_internal',
            'source_email_internal',
            'source_organization',
            'source_name_public',
            'source_email_public',
            'source_email_person_responsible',
            'source_role_person_responsible',
            'update_method',
            'update_frequency',
            'last_updated',
            'authorization_level',
            'status',
            'show_in_overview',
            'access_constraints',
            'other_constraints',
            'usage_constraints',
            'meta_email_internal',
            'meta_organization',
            'meta_email_person_responsible',
            'meta_role_person_responsible',
        ]


class LayerSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')
    source = SourceSerializer(source='layer_source')
    opacity = serializers.SerializerMethodField('get_opacity')
    zoom_min = serializers.SerializerMethodField('get_zoom_min')
    zoom_max = serializers.SerializerMethodField('get_zoom_max')
    display_properties = serializers.SerializerMethodField(
        'get_display_properties')
    search_properties = serializers.SerializerMethodField(
        'get_search_properties')
    search_terms = serializers.SerializerMethodField(
        'get_search_terms')
    metadata = MetadataSerializerField(source='*')
    linked_data = LinkedDataSerializer(many=True)
    related_tables = serializers.SerializerMethodField('get_related_tables')
    templates = TemplateSerializer(many=True)

    def get_can_access(self, obj):
        request = self.context['request']
        return can_request_access_layer(request, obj)

    def get_related_tables(self, obj):
        from tables_v2.serializers import TableTempSerializer

        tables = obj.related_tables.all()
        return TableTempSerializer(tables, many=True, from_layer=obj).data

    def get_opacity(self, obj):
        return float(obj.opacity)

    def get_zoom_min(self, obj):
        return safe_float_or_null(obj.zoom_min)

    def get_zoom_max(self, obj):
        return safe_float_or_null(obj.zoom_max)

    def get_display_properties(self, obj):
        return obj.popup_attributes

    def get_search_properties(self, obj):
        return obj.search_fields

    def get_search_terms(self, obj):
        return obj.search_terms

    class Meta:
        model = Layer
        fields = [
            'id',
            'source_type',
            'title',
            'description',
            'can_access',
            'slug',
            'layer_name',
            'opacity',
            'server_style',
            'client_style',
            'friendly_fields',
            'is_base',
            'is_visible',
            'is_selectable',
            'show_in_detail_panel',
            'use_html_info_format',
            'not_in_atlas',
            'extent_min_x',
            'extent_min_y',
            'extent_max_x',
            'extent_max_y',
            'closed_dataset',
            'login_required',
            'projection',
            'extent',
            'format',
            'zoom_min',
            'zoom_max',
            'category',
            'source',
            'server_type',
            'server_style',
            'client_style',
            'friendly_fields',
            'templated_properties',
            'legend_url',
            'display_properties',
            'search_properties',
            'search_terms',
            'metadata',
            'linked_data',
            'templates',
            'atlas_groups',
            'atlas_write_groups',
            'published',
            'templated_properties',
            'dataset',
            'metadataset',
            'is_filterable_in_legend',
            'authenticated_can_mutate',
            'is_exportable',
            'related_tables'
        ]


class LayerCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source='layer_type', queryset=Category.objects.all(), allow_null=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source='layer_source', queryset=Source.objects.all())
    metadata = MetadataSerializerField(source='*')
    linked_data = LinkedDataSerializer(many=True, required=False)
    templates = TemplateSerializer(many=True, required=False)
    display_properties = serializers.ListField(
        child=serializers.CharField(), required=False)
    search_properties = serializers.ListField(
        child=serializers.CharField(), required=False)
    search_terms = serializers.ListField(
        child=serializers.CharField(), required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['display_properties'] = instance.popup_attributes
        ret['search_properties'] = instance.search_fields
        ret['search_terms'] = instance.search_terms
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['_popup_attributes'] = '\r\n'.join(data.get('display_properties', []))
        ret['_search_fields'] = '\r\n'.join(data.get('search_properties', []))
        ret['_search_terms'] = '\r\n'.join(data.get('search_terms', []))
        return ret

    def update(self, instance, validated_data):
        linked_data, templates = (validated_data.pop(key, None)
                                  for key in ('linked_data', 'templates'))

        # Handling many-to-many field 'atlas_groups'
        if 'atlas_groups' in validated_data:
            atlas_groups_data = validated_data.pop('atlas_groups')
            instance.atlas_groups.set(atlas_groups_data)

        # Remove search_terms from validated_data if it exists since we handle it separately
        validated_data.pop('search_terms', None)

        if 'atlas_write_groups' in validated_data:
            atlas_write_groups_data = validated_data.pop('atlas_write_groups')
            instance.atlas_write_groups.set(atlas_write_groups_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Handling many-to-many field 'linked_data'
        if linked_data is not None:
            linked_data_to_create = []
            for data in linked_data:
                linked_data_to_create.append(LinkedData(
                    source=data.get('source'),
                    title=data.get('title'),
                    layer_name=data.get('layer_name'),
                    url=data.get('url'),
                    source_key=data.get('source_key'),
                    target_key=data.get('target_key'),
                    popup_attributes=data.get('popup_attributes'),
                    headers=data.get('headers'),
                    use_detail_view=data.get('use_detail_view'),
                    detail_view_fields=data.get('detail_view_fields'),
                ))

            instance.linked_data.all().delete()
            instance.linked_data.set(linked_data_to_create, bulk=False)

        # Handling many-to-many field 'templates'
        if templates is not None:
            templates_data_to_create = []
            for data in templates:
                templates_data_to_create.append(Template(
                    source=data.get('source'),
                    endpoint=data.get('endpoint'),
                    method=data.get('method'),
                    title=data.get('title'),
                    list=data.get('list'),
                    template=data.get('template'),
                    fields=data.get('fields'),
                    headers=data.get('headers'),
                ))

            instance.templates.all().delete()
            instance.templates.set(templates_data_to_create, bulk=False)

        return instance

    class Meta:
        model = Layer
        fields = [
            'id',
            'title',
            'description',
            'slug',
            'category_id',
            'source_id',
            'layer_source',
            'layer_name',
            'source_type',
            'projection',
            'server_type',
            'format',
            'opacity',
            'is_base',
            'is_visible',
            'is_selectable',
            'use_html_info_format',
            'show_in_detail_panel',
            'not_in_atlas',
            'display_properties',
            'search_properties',
            'extent_min_x',
            'extent_min_y',
            'extent_max_x',
            'extent_max_y',
            'zoom_min',
            'zoom_max',
            'server_style',
            'client_style',
            'friendly_fields',
            'templated_properties',
            'legend_url',
            'search_terms',
            'metadata',
            'login_required',
            'closed_dataset',
            'ordering',
            'atlas_groups',
            'atlas_write_groups',
            'published',
            'linked_data',
            'templates',
            'dataset',
            'metadataset',
            'is_filterable_in_legend',
            'is_exportable',
            'authenticated_can_mutate'
        ]


class LayerListSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')
    metadataset = MetadatasetSerializer(read_only=True)

    def get_can_access(self, obj):
        request = self.context['request']
        return can_request_access_layer(request, obj)

    class Meta:
        model = Layer
        fields = [
            'id',
            'source_type',
            'title',
            'can_access',
            'slug',
            'layer_name',
            'category',
            'published',
            'ordering',
            'is_base',
            'is_visible',
            'login_required',
            'closed_dataset',
            'metadataset'
        ]


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'features']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasGroup
        fields = ['id', 'name', 'slug', 'external_id']


class UserSerializer(serializers.ModelSerializer):
    atlas_groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = AtlasUser
        fields = ['id', 'username', 'name', 'email', 'is_staff', 'is_active',
                  'is_superuser', 'atlas_groups', 'external_id', 'date_joined', 'last_login']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasUser
        fields = ['id', 'username', 'name', 'email', 'is_staff', 'is_active',
                  'is_superuser', 'atlas_groups', 'external_id', 'date_joined', 'last_login']


class DataExportSettingsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class DuplicateSettingsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class DeleteSettingsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class BasicThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title', 'slug']


class DatasetSerializer(serializers.ModelSerializer):
    layers = LayerSerializer(many=True)
    themes = BasicThemeSerializer(many=True, read_only=True)
    dataset_category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'organization', 'dataset_category', 'source_description', 'purpose_of_manufacture',
                  'description',
                  'title', 'contact', 'data_owner', 'data_controller', 'last_updated', 'update_frequency', 'layers',
                  'themes', 'slug', 'thumbnail', 'published', 'show_in_overview']


class DatasetPatchOrCreateSerializer(serializers.ModelSerializer):
    themes = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), many=True)

    class Meta:
        model = Dataset
        fields = ['organization', 'dataset_category', 'source_description', 'purpose_of_manufacture', 'description',
                  'title',
                  'contact', 'data_owner', 'data_controller', 'last_updated', 'update_frequency', 'themes', 'id',
                  'slug', 'published', 'show_in_overview']
        read_only_fields = ['id']


class BasicDatasetSerializer(serializers.ModelSerializer):
    layers = LayerSerializer(many=True)

    class Meta:
        model = Dataset
        fields = ['id', 'organization', 'dataset_category', 'source_description', 'purpose_of_manufacture',
                  'description', 'title',
                  'contact', 'data_owner', 'data_controller', 'last_updated', 'update_frequency', 'layers', 'slug',
                  'published', 'show_in_overview']


class ThemeSerializer(serializers.ModelSerializer):
    datasets = BasicDatasetSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['id', 'title', 'datasets', 'slug']


class ThemePatchOrCreateSerializer(serializers.ModelSerializer):
    datasets = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all(), many=True)

    class Meta:
        model = Theme
        fields = ['title', 'datasets', 'id', 'slug']
        read_only_fields = ['slug', 'id']

    def update(self, instance, validated_data):
        if 'title' in validated_data and validated_data['title'] != instance.title:
            instance.slug = slugify(validated_data['title'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class ViewerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        self.title = obj.label
        return self.title

    class Meta:
        model = Viewer
        fields = ['ordering', 'label', 'type', 'username', 'password', 'api_key', 'url', 'is_oblique', 'internal', 'id',
                  'type', 'title']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'username', 'user_agent', 'email', 'ip', 'source', 'resource', 'params', 'time_created']
