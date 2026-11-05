from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from table.models import LayerToTable, Table
from webservice.models import Category, Layer, Map, MapLayer, Source
from webservice.serializers import LayerCreateUpdateSerializer, LayerSerializer


class LayerSerializerTest(APITestCase):
    def setUp(self):
        self.source = Source.objects.create(slug='test-source', title='Test Source', url='http://test.com')
        self.category = Category.objects.create(slug='test-category', title='Test Category')

    def get_request(self):
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        return request

    def test_serializes_assigned_maps(self):
        """Return the ids of maps that currently use this layer."""
        layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=self.source,
            layer_type=self.category,
        )
        map_instance = Map.objects.create(title='Map 1', slug='map-1')
        MapLayer.objects.create(map=map_instance, layer=layer, settings={})

        serializer = LayerSerializer(instance=layer, context={'request': self.get_request()})

        self.assertEqual(serializer.data['assigned_maps'], [map_instance.id])

    def test_serializes_related_tables_by_relation_order(self):
        """Return related tables in saved order with their relation settings."""
        layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=self.source,
            layer_type=self.category,
        )
        first_table = Table.objects.create(
            title='Z Table',
            slug='z-table',
            source=self.source,
            layer_name='z:table',
        )
        second_table = Table.objects.create(
            title='A Table',
            slug='a-table',
            source=self.source,
            layer_name='a:table',
        )
        LayerToTable.objects.create(from_layer=layer, to_table=first_table, field_mapping={}, ordering=2)
        second_relation = LayerToTable.objects.create(
            from_layer=layer,
            to_table=second_table,
            field_mapping={"source": "target"},
            related_table_title="Custom title",
            ordering=1,
        )

        serializer = LayerSerializer(instance=layer, context={'request': self.get_request()})

        self.assertEqual(
            [table['title'] for table in serializer.data['related_tables']],
            ['A Table', 'Z Table'],
        )
        self.assertEqual(serializer.data['related_tables'][0]['layer_to_table_id'], second_relation.id)
        self.assertEqual(serializer.data['related_tables'][0]['field_mapping'], {"source": "target"})
        self.assertEqual(serializer.data['related_tables'][0]['related_table_title'], "Custom title")
        self.assertEqual(serializer.data['related_tables'][0]['ordering'], 1)

    def test_to_dict_serializes_related_tables_by_relation_order(self):
        """Keep related tables in saved order in the layer dictionary output."""
        layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=self.source,
            layer_type=self.category,
        )
        first_table = Table.objects.create(
            title='Z Table',
            slug='z-table',
            source=self.source,
            layer_name='z:table',
        )
        second_table = Table.objects.create(
            title='A Table',
            slug='a-table',
            source=self.source,
            layer_name='a:table',
        )
        LayerToTable.objects.create(from_layer=layer, to_table=first_table, field_mapping={}, ordering=2)
        LayerToTable.objects.create(from_layer=layer, to_table=second_table, field_mapping={}, ordering=1)

        data = layer.to_dict(AnonymousUser(), self.get_request())

        self.assertEqual(
            [table['title'] for table in data['related_tables']],
            ['A Table', 'Z Table'],
        )


class LayerCreateUpdateSerializerTest(APITestCase):
    def setUp(self):
        self.source = Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com',
        )
        self.category = Category.objects.create(
            slug='test-category',
            title='Test Category',
            ordering=2,
        )
        self.layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=self.source,
            layer_type=self.category,
        )
        self.map_instance = Map.objects.create(title='Map 1', slug='map-1')

    def update_layer(self, payload):
        serializer = LayerCreateUpdateSerializer(instance=self.layer, data=payload, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def test_map_ids_require_layer_category_when_adding_to_map(self):
        """Reject a map assignment when the layer has no category."""
        self.layer.layer_type = None
        self.layer.save()

        serializer = LayerCreateUpdateSerializer(
            instance=self.layer,
            data={'map_ids': [self.map_instance.id]},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('map_ids', serializer.errors)

    def test_map_ids_updates_layer_map_assignments(self):
        """Create the map assignment sent in the layer update request."""
        self.update_layer({'map_ids': [self.map_instance.id]})

        self.assertTrue(MapLayer.objects.filter(map=self.map_instance, layer=self.layer).exists())

    def test_patch_without_map_ids_does_not_change_existing_assignments(self):
        """Keep existing map assignments when a patch does not send map ids."""
        MapLayer.objects.create(map=self.map_instance, layer=self.layer, settings={})

        self.update_layer({'title': 'Updated Layer'})

        self.assertTrue(MapLayer.objects.filter(map=self.map_instance, layer=self.layer).exists())

    def test_empty_map_ids_removes_existing_assignments(self):
        """Remove all map assignments when the update sends an empty list."""
        MapLayer.objects.create(map=self.map_instance, layer=self.layer, settings={})

        self.update_layer({'map_ids': []})

        self.assertFalse(MapLayer.objects.filter(map=self.map_instance, layer=self.layer).exists())

    def test_related_tables_updates_ordering(self):
        """Update the saved order of one existing related table."""
        table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        relation = LayerToTable.objects.create(from_layer=self.layer, to_table=table, field_mapping={}, ordering=5)

        self.update_layer({
            'related_tables': [{
                'id': relation.id,
                'to_table': table.id,
                'field_mapping': {},
                'ordering': 0,
            }]
        })

        relation.refresh_from_db()
        self.assertEqual(relation.ordering, 0)

    def test_empty_related_tables_removes_relations(self):
        """Remove all layer table relations when the update sends an empty list."""
        table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        LayerToTable.objects.create(from_layer=self.layer, to_table=table, field_mapping={})

        self.update_layer({'related_tables': []})

        self.assertFalse(LayerToTable.objects.filter(from_layer=self.layer).exists())

    def test_patch_without_related_tables_keeps_existing_relations(self):
        """Keep existing table relations when a patch does not send them."""
        table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        relation = LayerToTable.objects.create(from_layer=self.layer, to_table=table, field_mapping={})

        self.update_layer({'title': 'Updated Layer'})

        self.assertTrue(LayerToTable.objects.filter(id=relation.id).exists())

    def test_related_tables_update_keeps_adds_and_removes_relations(self):
        """Keep one relation, remove one, add one, and update its settings."""
        kept_table = Table.objects.create(
            title='Kept table', slug='kept-table', source=self.source, layer_name='kept:table'
        )
        removed_table = Table.objects.create(
            title='Removed table', slug='removed-table', source=self.source, layer_name='removed:table'
        )
        added_table = Table.objects.create(
            title='Added table', slug='added-table', source=self.source, layer_name='added:table'
        )
        kept_relation = LayerToTable.objects.create(from_layer=self.layer, to_table=kept_table, field_mapping={})
        removed_relation = LayerToTable.objects.create(from_layer=self.layer, to_table=removed_table, field_mapping={})

        self.update_layer(
            {
                'related_tables': [
                    {
                        'id': kept_relation.id,
                        'to_table': kept_table.id,
                        'field_mapping': {'old': 'new'},
                        'related_table_title': 'Kept title',
                        'ordering': 1,
                    },
                    {'to_table': added_table.id, 'field_mapping': {}, 'ordering': 2},
                ]
            }
        )

        kept_relation.refresh_from_db()
        self.assertEqual(kept_relation.field_mapping, {'old': 'new'})
        self.assertEqual(kept_relation.related_table_title, 'Kept title')
        self.assertEqual(kept_relation.ordering, 1)
        self.assertFalse(LayerToTable.objects.filter(id=removed_relation.id).exists())
        self.assertTrue(LayerToTable.objects.filter(from_layer=self.layer, to_table=added_table).exists())
