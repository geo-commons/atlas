from rest_framework import serializers

from tables_v2.models import TableTemp, TableToTable
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
            'related_tables'
        ]
