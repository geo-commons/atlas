from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from rest_framework.test import APITestCase

from table.models import LayerToTable, Table, TableToTable
from webservice.models import Category, Layer, Map, MapCategory, MapLayer, Source


class DeleteProtectionTest(APITestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)

    def create_source(self, title='Source'):
        return Source.objects.create(
            title=title,
            slug=title.lower().replace(' ', '-'),
            url='https://example.com/ows',
        )

    def create_layer(self, source, title='Layer', category=None):
        return Layer.objects.create(
            title=title,
            slug=title.lower().replace(' ', '-'),
            layer_name=f'atlas:{title.lower().replace(" ", "_")}',
            layer_source=source,
            layer_type=category,
        )

    def test_source_delete_returns_clear_error_when_used_by_layer(self):
        source = self.create_source()
        layer = self.create_layer(source)

        response = self.client.delete(f'/atlas/api/v1/sources/{source.id}/')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['code'], 'protected_delete')
        self.assertEqual(response.data['protected_by'], ['Kaartlagen'])
        self.assertEqual(
            response.data['protected_objects'],
            [
                {
                    'type': 'Kaartlagen',
                    'objects': [{'id': layer.id, 'label': layer.title}],
                    'remaining_count': 0,
                }
            ],
        )
        self.assertIn(f'Kaartlagen: {layer.title}', response.data['detail'])
        self.assertTrue(Source.objects.filter(pk=source.pk).exists())
        self.assertEqual(Layer.objects.get(pk=layer.pk).layer_source_id, source.pk)

    def test_bulk_source_delete_is_blocked_when_used_by_table(self):
        source = self.create_source()
        Table.objects.create(title='Table', slug='table', source=source, layer_name='atlas:table')

        response = self.client.post('/atlas/api/v1/sources/delete/', {'ids': [source.id]}, format='json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['protected_by'], ['Tabellen'])
        self.assertTrue(Source.objects.filter(pk=source.pk).exists())

    def test_layer_delete_is_blocked_when_it_is_on_a_map(self):
        source = self.create_source()
        layer = self.create_layer(source)
        map_instance = Map.objects.create(title='Map', slug='map')
        MapLayer.objects.create(layer=layer, map=map_instance, settings={})

        response = self.client.delete(f'/atlas/api/v1/layers/{layer.id}/')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['protected_by'], ['Kaartlagen'])
        self.assertTrue(Layer.objects.filter(pk=layer.pk).exists())
        self.assertTrue(MapLayer.objects.filter(layer=layer, map=map_instance).exists())

    def test_category_delete_is_blocked_when_used_by_a_map(self):
        category = Category.objects.create(title='Category', slug='category')
        map_instance = Map.objects.create(title='Map', slug='map')
        MapCategory.objects.create(category=category, map=map_instance)

        response = self.client.delete(f'/atlas/api/v1/categories/{category.id}/')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['protected_by'], ['Kaartcategorieën'])
        self.assertTrue(Category.objects.filter(pk=category.pk).exists())

    def test_table_relationships_protect_both_tables_and_layers(self):
        source = self.create_source()
        category = Category.objects.create(title='Category', slug='category')
        layer = self.create_layer(source, category=category)
        table = Table.objects.create(title='Table', slug='table', source=source, layer_name='atlas:table')
        related_table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=source,
            layer_name='atlas:related_table',
        )
        LayerToTable.objects.create(from_layer=layer, to_table=table, field_mapping={'id': 'id'})
        TableToTable.objects.create(from_table=table, to_table=related_table, field_mapping={'id': 'id'})

        with self.assertRaises(ProtectedError):
            layer.delete()
        with self.assertRaises(ProtectedError):
            table.delete()
        with self.assertRaises(ProtectedError):
            related_table.delete()
