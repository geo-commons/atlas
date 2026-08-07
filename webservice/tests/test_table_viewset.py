from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from table.models import LayerToTable, Table, TableToTable
from webservice.models import Category, Layer, Source


class TableViewSetTest(APITestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)

    def test_duplicate_skips_explicit_through_relations(self):
        source = Source.objects.create(
            title='Table source',
            slug='table-source',
            url='https://example.com/ows',
        )
        category = Category.objects.create(title='Table category', slug='table-category')
        layer = Layer.objects.create(
            title='Related layer',
            slug='related-layer',
            layer_name='related:layer',
            layer_source=source,
            layer_type=category,
        )
        table = Table.objects.create(
            title='Original table',
            slug='original-table',
            source=source,
            layer_name='original:table',
        )
        related_table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=source,
            layer_name='related:table',
        )
        LayerToTable.objects.create(
            from_layer=layer,
            to_table=table,
            field_mapping={'id': 'id'},
        )
        TableToTable.objects.create(
            from_table=table,
            to_table=related_table,
            field_mapping={'id': 'id'},
        )

        response = self.client.post(
            '/atlas/api/v1/tables/duplicate/',
            {'ids': [table.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        duplicated_table = Table.objects.get(title='Original table (2)')
        self.assertFalse(LayerToTable.objects.filter(to_table=duplicated_table).exists())
        self.assertFalse(TableToTable.objects.filter(from_table=duplicated_table).exists())
