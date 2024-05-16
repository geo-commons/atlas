from rest_framework import serializers
from user_management.models import AtlasGroup, AtlasUser
from .models import Category, Drawing, LinkedData, Map, MapLayer, Source, Layer, Template
from authz.lib import can_request_access_layer


class MapLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLayer
        fields = ['layer', 'settings']


class MapSerializer(serializers.ModelSerializer):
    layers = MapLayerSerializer(many=True, source='map_layers')

    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers']

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
        fields = ['id', 'title', 'slug', 'url', 'authenticate', 'source_type']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'ordering']


class LinkedDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='layer_name')
    display_properties = serializers.SerializerMethodField('get_display_properties')
    headers = serializers.SerializerMethodField('get_headers')

    def get_display_properties(self, obj):
        return obj.popup_attributes.split('\r\n') if obj.popup_attributes else []

    def get_headers(self, obj):
        return obj.headers.split('\r\n') if obj.headers else []

    class Meta:
        model = LinkedData
        fields = ['id', 'title', 'name', 'url', 'source_key', 'target_key', 'headers', 'display_properties']



class TemplateSerializer(serializers.ModelSerializer):
    source = SourceSerializer()
    fields = serializers.SerializerMethodField('get_template_fields')
    headers = serializers.SerializerMethodField('get_headers')

    def get_template_fields(self, obj):
        return obj.fields.split('\r\n') if obj.fields else []

    def get_headers(self, obj):
        return obj.headers.split('\r\n') if obj.headers else []
    
    class Meta:
        model = Template
        fields = ['id', 'title', 'source', 'endpoint', 'method', 'list', 'headers', 'fields', 'template', 'ordering']


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
            'meta_contact': data['contact']
        }


class LayerSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')
    source = SourceSerializer(source='layer_source')
    opacity = serializers.SerializerMethodField('get_opacity')
    display_properties = serializers.SerializerMethodField(
        'get_display_properties')
    search_properties = serializers.SerializerMethodField(
        'get_search_properties')
    metadata = MetadataSerializerField(source='*')
    linked_data = LinkedDataSerializer(many=True)
    templates = TemplateSerializer(many=True)

    def get_can_access(self, obj):
        request = self.context['request']
        return can_request_access_layer(request, obj)

    def get_opacity(self, obj):
        return float(obj.opacity)

    def get_display_properties(self, obj):
        return obj.popup_attributes

    def get_search_properties(self, obj):
        return obj.search_fields

    class Meta:
        model = Layer
        fields = [
            'id',
            'source_type',
            'title',
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
            'display_properties',
            'search_properties',
            'metadata',
            'linked_data',
            'templates',
            'atlas_groups',
            'published',
            'templated_properties'
        ]


class LayerCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source='layer_type', queryset=Category.objects.all(), allow_null=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source='layer_source', queryset=Source.objects.all())
    metadata = MetadataSerializerField(source='*')

    class Meta:
        model = Layer
        fields = [
            'id',
            'title',
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
            'zoom_min',
            'zoom_max',
            'metadata',
            'login_required',
            'closed_dataset',
            'ordering',
            'atlas_groups',
            'published'
        ]


class LayerListSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')

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
        ]


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'features']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasUser
        fields = ['id', 'username', 'name', 'email', 'is_staff', 'is_active',
                  'is_superuser', 'atlas_groups', 'external_id', 'date_joined', 'last_login']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasGroup
        fields = ['id', 'name', 'slug', 'external_id']


class DataExportSettingsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
