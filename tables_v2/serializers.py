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
            'id',
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
    related_tables = serializers.SerializerMethodField()

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

    def get_related_tables(self, obj):
        return TableToTableSerializer(obj.outgoing_table_relations, many=True).data

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if 'related_tables' in data:
            ret['related_tables'] = data['related_tables']
        return ret

    def update(self, instance, validated_data):
        related_tables = validated_data.pop('related_tables', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if related_tables:
            try:
                incoming_table_ids = {item.get('id') for item in related_tables if item.get('id')}
                existing_relations = TableToTable.objects.filter(from_table=instance)
                relations_to_delete = existing_relations.exclude(id__in=incoming_table_ids)
                relations_to_delete.delete()

                for item in related_tables:
                    relation_id = item.get('id')
                    if relation_id:
                        existing_relation = TableToTable.objects.get(id=relation_id)
                        field_mapping = item.get('field_mapping')
                        if field_mapping is not None:
                            existing_relation.field_mapping = field_mapping
                            existing_relation.save()
                    else:
                        TableToTable.objects.create(
                            from_table=instance,
                            to_table_id=item.get('to_table'),
                            field_mapping=item.get('field_mapping')
                        )
            except Exception as e:
                raise serializers.ValidationError({
                    'related_tables': 'Er is een onverwachte fout opgretreden bij het opslaan van de gerelateerde tabellen. '
                                      f'Error details: {str(e)}'
                })
        return instance

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
