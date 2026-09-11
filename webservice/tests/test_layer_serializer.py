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

        serializer = LayerSerializer(instance=layer, context={'request': self.get_request()})

        self.assertEqual(
            [table['title'] for table in serializer.data['related_tables']],
            ['A Table', 'Z Table'],
        )

    def test_to_dict_serializes_related_tables_by_relation_order(self):
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
        self.update_layer({'map_ids': [self.map_instance.id]})

        self.assertTrue(MapLayer.objects.filter(map=self.map_instance, layer=self.layer).exists())

    def test_patch_without_map_ids_does_not_change_existing_assignments(self):
        MapLayer.objects.create(map=self.map_instance, layer=self.layer, settings={})

        self.update_layer({'title': 'Updated Layer'})

        self.assertTrue(MapLayer.objects.filter(map=self.map_instance, layer=self.layer).exists())

    def test_related_tables_updates_ordering(self):
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
        table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        LayerToTable.objects.create(from_layer=self.layer, to_table=table, field_mapping={})

        self.update_layer({'related_tables': []})

        self.assertFalse(LayerToTable.objects.filter(from_layer=self.layer).exists())
