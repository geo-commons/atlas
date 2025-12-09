from rest_framework import serializers

from tables_v2.models import TableTemp, TableToTable, LayerToTable
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
            'list_cql_filters',
            'detail_cql_filters',
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
            'source_type',
            'fields',
            'list_endpoint',
            'detail_endpoint',
            'list_cql_filters',
            'detail_cql_filters',
            'related_tables',
            'field_mapping'
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
