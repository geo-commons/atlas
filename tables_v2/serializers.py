from rest_framework import serializers

from tables_v2.models import TableTemp, TableToTable, LayerToTable
from webservice.models import Source
from webservice.serializers import SourceSerializer


class SimpleTableTempSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)

    class Meta:
        model = TableTemp
        fields = [
            'id',
            'title',
            'slug',
            'source',
            'source_type',
            'fields',
            'list_endpoint',
            'detail_endpoint',
            'list_property',
            'detail_property',
            'page_param',
            'items_per_page_param',
            'total_items_page_property',
            'list_error_property',
            'detail_error_property',
            'layer_name',
            'list_cql_filters',
            'detail_cql_filters',
            'list_display_properties',
            'detail_display_properties',
            'template_fields',
        ]


class TableToTableSerializer(serializers.ModelSerializer):
    to_table = SimpleTableTempSerializer()

    class Meta:
        model = TableToTable
        fields = [
            'to_table',
            'field_mapping',
        ]


class LayerToTableSerializer(serializers.ModelSerializer):
    # to_table = SimpleTableTempSerializer()

    class Meta:
        unique_together = ('from_layer', 'to_table')
        model = LayerToTable
        fields = [
            'field_mapping',
        ]


class TableTempSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source='source', queryset=Source.objects.all())
    field_mapping = serializers.SerializerMethodField()
    layer_to_table_id = serializers.SerializerMethodField()

    related_tables = TableToTableSerializer(
        source='outgoing_table_relations',
        many=True,
        read_only=True
    )

    class Meta:
        model = TableTemp
        fields = [
            'id',
            'title',
            'slug',
            'source',
            'source_id',
            'source_type',
            'fields',
            'list_endpoint',
            'detail_endpoint',
            'list_property',
            'detail_property',
            'page_param',
            'items_per_page_param',
            'total_items_page_property',
            'list_error_property',
            'detail_error_property',
            'list_cql_filters',
            'detail_cql_filters',
            'related_tables',
            'field_mapping',
            'layer_name',
            'list_display_properties',
            'detail_display_properties',
            'template_fields',
            'layer_to_table_id',
        ]

    def _get_layer_to_table(self, obj):
        """Helper method to get LayerToTable object"""
        from_layer = self.context.get('from_layer')
        if from_layer:
            return LayerToTable.objects.filter(
                from_layer=from_layer,
                to_table=obj
            ).first()
        return None

    def get_field_mapping(self, obj):
        """Include field_mapping from LayerToTable if called from a Layer context"""
        layer_to_table = self._get_layer_to_table(obj)
        return layer_to_table.field_mapping if layer_to_table else None

    def get_layer_to_table_id(self, obj):
        """Include LayerToTable ID for editing relations"""
        layer_to_table = self._get_layer_to_table(obj)
        return layer_to_table.id if layer_to_table else None
