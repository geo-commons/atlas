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
        ]


class TableToTableSerializer(serializers.ModelSerializer):
    to_table = SimpleTableTempSerializer()

    class Meta:
        model = TableToTable
        fields = [
            'to_table',
            'field_mapping',
        ]


class TableTempSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source='source', queryset=Source.objects.all())
    field_mapping = serializers.SerializerMethodField()

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
        ]

    def __init__(self, *args, from_layer=None, **kwargs):
        self.from_layer = from_layer
        super().__init__(*args, **kwargs)

    def get_field_mapping(self, obj):
        """Include field_mapping from LayerToTable if called from a Layer context"""
        if self.from_layer:
            try:
                layer_to_table = LayerToTable.objects.get(from_layer=self.from_layer, to_table=obj)
                return layer_to_table.field_mapping
            except LayerToTable.DoesNotExist:
                return None
        return None
