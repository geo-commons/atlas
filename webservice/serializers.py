from rest_framework import serializers

from .models import Category, Drawing, LinkedData, Map, Source, Layer, Template
from .authorization import can_request_access_layer


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title', 'slug', 'url', 'authenticate']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'ordering']

class LinkedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedData
        fields = ['id', 'title', 'layer_name']

class TemplateSerializer(serializers.ModelSerializer):
    source = SourceSerializer()

    class Meta:
        model = Template
        fields = ['id', 'title', 'source']


class MetadataSerializerField(serializers.Field):

    def to_representation(self, value):
        return {
            'name': value.meta_name,
            'description': value.meta_description,
            'organization': value.meta_org,
            'updated': value.meta_updated,
            'link': value.meta_link
        }          

    def to_internal_value(self, data):
        return {
            'meta_name': data['name'],
            'meta_description': data['description'],
            'meta_org': data['organization'],
            'meta_updated': data['updated'],
            'meta_link': data['link']
        }

class LayerSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')
    source = SourceSerializer(source='layer_source')
    opacity = serializers.SerializerMethodField('get_opacity')
    display_properties = serializers.SerializerMethodField('get_display_properties')
    search_properties = serializers.SerializerMethodField('get_search_properties')
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
            'templates'
        ]

class LayerCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(source='layer_type', queryset=Category.objects.all())
    source_id = serializers.PrimaryKeyRelatedField(source='layer_source', queryset=Source.objects.all())
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
            'ordering'
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
            'ordering'
        ]


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'features']
