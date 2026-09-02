from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from authz.lib import can_request_access_layer
from authz.models import Log
from user_management.models import AtlasGroup, AtlasUser
from .models import (
    Category,
    Drawing,
    Layer,
    LinkedData,
    Map,
    MapLayer,
    MapCategory,
    Metadataset,
    Source,
    Template,
    Viewer,
)
from .util import safe_float_or_null


class MapLayerSerializer(serializers.ModelSerializer):
    map_category = serializers.PrimaryKeyRelatedField(
        queryset=MapCategory.objects.none(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = MapLayer
        fields = ['layer', 'settings', 'is_base', 'is_visible', 'ordering', 'map_category']


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Category.objects.all(),
        allow_null=True,
        required=False,
    )
    parent = serializers.SerializerMethodField()
    full_title = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if not obj.parent:
            return None

        return {
            'id': obj.parent.id,
            'title': obj.parent.title,
            'slug': obj.parent.slug,
        }

    def get_full_title(self, obj):
        return obj.full_title

    def validate(self, attrs):
        category = self.instance if self.instance else Category()
        
        for attr, value in attrs.items():
            setattr(category, attr, value)

        try:
            category.clean()
        except DjangoValidationError as exc:
            errors = exc.message_dict
            if "parent" in errors:
                errors["parent_id"] = errors.pop("parent")
            raise serializers.ValidationError(errors) from exc
        
        return attrs

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'ordering', 'parent', 'parent_id', 'full_title']


class MapCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = MapCategory
        fields = ['id', 'category', 'title', 'ordering']

    def get_title(self, obj):
        return obj.category.title if obj.category else ""


class MapSerializer(serializers.ModelSerializer):
    layers = MapLayerSerializer(many=True, source='map_layers', required=False)
    categories = MapCategorySerializer(many=True, source='map_categories', required=False)

    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers', 'categories', 'thumbnail', 'description',
                  'keywords',
                  'published', 'show_in_overview', 'about', 'about_title', 'is_main']
        read_only_fields = ['is_main']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 'child' is the MapLayerSerializer instance.
        layer_serializer = self.fields['layers'].child

        # Only apply queryset scoping during writes.
        # On read/list endpoints `self.instance` can be a queryset/list, not a single Map.
        if not hasattr(self, 'initial_data'):
            return

        # Scope the allowed 'map_category' ids to the current map on updates.
        # This prevents cross-map references (e.g., assigning a category from map B to a layer on map A).
        if isinstance(self.instance, Map):
            layer_serializer.fields['map_category'].queryset = self.instance.map_categories.all()
            return

        # During create there is no map yet, so there cannot be valid existing MapCategory ids.
        # We therefore disallow explicit ids here and rely on fallback resolution in create()
        # (`layer.layer_type_id` -> matching map category created in this request).
        layer_serializer.fields['map_category'].queryset = MapCategory.objects.none()

    def create(self, validated_data):
        map_layers = validated_data.pop('map_layers', [])
        map_categories = validated_data.pop('map_categories', [])

        created_map = Map.objects.create(**validated_data)

        self._sync_categories(created_map, map_categories)
        self._sync_layers(created_map, map_layers)

        return created_map

    def update(self, instance, validated_data):
        has_layers = "map_layers" in validated_data
        has_categories = "map_categories" in validated_data
        map_layers = validated_data.pop("map_layers", [])
        map_categories = validated_data.pop("map_categories", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if has_categories:
            self._sync_categories(instance, map_categories)

        if has_layers:
            self._sync_layers(instance, map_layers)

        return instance

    def _sync_categories(self, map_instance, map_categories):
        kept_category_ids = []
        for map_category in map_categories:
            category = map_category.get("category")
            defaults = {
                "category": category,
                "ordering": map_category.get("ordering", 0),
                "map": map_instance,
            }

            obj, _ = MapCategory.objects.update_or_create(map=map_instance, category=category, defaults=defaults)

            kept_category_ids.append(obj.id)

            if category.parent_id:
                # Legacy payloads can submit only the subcategory. Keep the parent MapCategory
                # persisted so map-specific parent ordering can exist before the next tree save.
                parent_obj, _ = MapCategory.objects.get_or_create(
                    map=map_instance,
                    category=category.parent,
                    defaults={'ordering': category.parent.ordering},
                )
                kept_category_ids.append(parent_obj.id)

        map_instance.map_categories.exclude(id__in=kept_category_ids).delete()

    def _sync_layers(self, map_instance, map_layers):
        kept_layer_ids = []
        for map_layer in map_layers:
            obj = self._update_or_create_map_layer(map_instance, map_layer)
            kept_layer_ids.append(obj.id)

        map_instance.map_layers.exclude(id__in=kept_layer_ids).delete()

    def _update_or_create_map_layer(self, map_instance, map_layer):
        layer = map_layer.get("layer")
        map_category = map_layer.get("map_category")

        if map_category is None and getattr(layer, "layer_type", None):
            map_category = map_instance.map_categories.filter(category_id=layer.layer_type_id).first()

        defaults = {
            "layer": layer,
            "map_category": map_category,
            "ordering": map_layer.get("ordering", 0),
            "settings": map_layer.get("settings", {}),
            "is_base": map_layer.get("is_base", False),
            "is_visible": map_layer.get("is_visible", False),
            "map": map_instance,
        }

        obj, _ = MapLayer.objects.update_or_create(map=map_instance, layer=layer, defaults=defaults)
        return obj


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title', 'slug', 'url', 'authenticate', 'source_type', 'atlas_groups', 'login_required']


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


class MetadatasetPublicSerializer(serializers.ModelSerializer):
    """Serializer for external/public API calls - excludes internal email addresses and sensitive fields"""
    layers = serializers.SerializerMethodField()

    def get_layers(self, obj):
        return obj.get_serialized_layers()

    class Meta:
        model = Metadataset
        fields = [
            'id',
            'title',
            'slug',
            'layers',
            'abstract',
            'topic_category',
            'keyword',
            'statement',
            'source_origin',
            'source_organization',
            'source_name_public',
            'source_email_public',
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


class MetadatasetNestedSerializer(serializers.ModelSerializer):
    """Metadataset fields exposed on layer APIs (excludes admin-only fme_script)."""
    layers = serializers.SerializerMethodField()

    def get_layers(self, obj):
        return obj.get_serialized_layers()

    class Meta:
        model = Metadataset
        fields = [
            'id',
            'title',
            'slug',
            'layers',
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


class MetadatasetSerializer(serializers.ModelSerializer):
    """Serializer for internal API calls - includes all fields including internal email addresses"""
    layers = serializers.SerializerMethodField()

    def get_layers(self, obj):
        return obj.get_serialized_layers()

    class Meta:
        model = Metadataset
        fields = MetadatasetNestedSerializer.Meta.fields + ['fme_script']


class LayerSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    assigned_maps = serializers.SerializerMethodField()
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
    linked_data = LinkedDataSerializer(many=True)
    related_tables = serializers.SerializerMethodField('get_related_tables')
    templates = TemplateSerializer(many=True)

    def get_can_access(self, obj):
        request = self.context['request']
        return can_request_access_layer(request, obj)

    def get_assigned_maps(self, obj):
        return list(obj.maps_layer.values_list('map_id', flat=True))

    def get_related_tables(self, obj):
        request = self.context['request']
        from table.serializers import TableSerializer

        tables = obj.related_tables.all()
        return TableSerializer(tables, many=True, context={'from_layer': obj, 'request': request}).data

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
            'is_selectable',
            'disable_highlighted_style',
            'show_in_detail_panel',
            'use_html_info_format',
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
            'linked_data',
            'templates',
            'atlas_groups',
            'atlas_write_groups',
            'templated_properties',
            'metadataset',
            'is_filterable_in_legend',
            'authenticated_can_mutate',
            'is_exportable',
            'related_tables',
            'is_time_enabled',
            'is_reference_date_enabled',
            'time_slider_default_display_mode',
            'time_slider_start_field',
            'time_slider_end_field',
            'assigned_maps',
        ]


class LayerCreateUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source='layer_type', queryset=Category.objects.all(), allow_null=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source='layer_source', queryset=Source.objects.all())
    linked_data = LinkedDataSerializer(many=True, required=False)
    templates = TemplateSerializer(many=True, required=False)
    display_properties = serializers.ListField(
        child=serializers.CharField(), required=False)
    search_properties = serializers.ListField(
        child=serializers.CharField(), required=False)
    search_terms = serializers.ListField(
        child=serializers.CharField(), required=False)
    map_ids = serializers.PrimaryKeyRelatedField(
        queryset=Map.objects.all(), many=True, write_only=True, required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if 'map_ids' not in attrs or not attrs['map_ids']:
            return attrs

        layer_type = attrs.get('layer_type') or getattr(self.instance, 'layer_type', None)
        if not layer_type:
            raise serializers.ValidationError({
                'map_ids': 'Selecteer eerst een categorie voordat je deze kaartlaag aan kaarten toevoegt.'
            })

        return attrs

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
        if 'related_tables' in data:
            ret['related_tables'] = data['related_tables']
        return ret

    def update(self, instance, validated_data):
        from table.models import LayerToTable

        linked_data, templates, related_tables, maps = (
            validated_data.pop(key, None)
            for key in ('linked_data', 'templates', 'related_tables', 'map_ids')
        )

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

        # Handling many-to-many field 'related_tables'
        if related_tables:
            try:
                # Get IDs of table relations sent in the request
                incoming_table_ids = {item.get('id') for item in related_tables}

                # Get existing relations
                existing_relations = LayerToTable.objects.filter(from_layer=instance)

                # Delete relations that are no longer needed
                relations_to_delete = existing_relations.exclude(id__in=incoming_table_ids)
                relations_to_delete.delete()

                for item in related_tables:
                    relation_id = item.get('id')

                    if relation_id:
                        # Update existing relation using its ID
                        existing_relation = LayerToTable.objects.get(id=relation_id)

                        field_mapping = item.get('field_mapping')
                        if field_mapping is not None:
                            existing_relation.field_mapping = field_mapping
                            
                        related_table_title = item.get('related_table_title')
                        if related_table_title is not None:
                            existing_relation.related_table_title = related_table_title
                            
                        existing_relation.save()
                    else:
                        # Create new relation
                        LayerToTable.objects.create(
                            from_layer=instance,
                            to_table_id=item.get('to_table'),
                            field_mapping=item.get('field_mapping')
                        )
            except Exception as e:
                raise serializers.ValidationError({
                    'related_tables': 'Er is een onverwachte fout opgretreden bij het opslaan van de gerelateerde tabellen. '
                                      f'Error details: {str(e)}'})

        if maps is not None:
            instance.sync_map_assignments(maps)

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
            'is_selectable',
            'disable_highlighted_style',
            'use_html_info_format',
            'show_in_detail_panel',
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
            'login_required',
            'closed_dataset',
            'ordering',
            'atlas_groups',
            'atlas_write_groups',
            'linked_data',
            'templates',
            'metadataset',
            'is_filterable_in_legend',
            'is_exportable',
            'authenticated_can_mutate',
            'related_tables',
            'is_time_enabled',
            'is_reference_date_enabled',
            'time_slider_default_display_mode',
            'time_slider_start_field',
            'time_slider_end_field',
            'map_ids',
        ]


class LayerListSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')
    category = CategorySerializer(source='layer_type')
    metadataset = MetadatasetNestedSerializer(read_only=True)

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
            'ordering',
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
