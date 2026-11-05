from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from table.models import Table, TableToTable
from table.serializers import TableSerializer
from webservice.models import Source


class TableSerializerTest(APITestCase):
    def setUp(self):
        self.source = Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com',
        )
        self.table = Table.objects.create(
            title='Parent table',
            slug='parent-table',
            source=self.source,
            layer_name='parent:table',
        )

    def get_request(self):
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        return request

    def test_serializes_related_tables_by_relation_order(self):
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
        TableToTable.objects.create(from_table=self.table, to_table=first_table, field_mapping={}, ordering=2)
        second_relation = TableToTable.objects.create(
            from_table=self.table,
            to_table=second_table,
            field_mapping={"source": "target"},
            related_table_title="Custom title",
            ordering=1,
        )

        serializer = TableSerializer(instance=self.table, context={'request': self.get_request()})

        self.assertEqual(
            [relation['to_table']['title'] for relation in serializer.data['related_tables']],
            ['A Table', 'Z Table'],
        )
        self.assertEqual(serializer.data['related_tables'][0]['id'], second_relation.id)
        self.assertEqual(serializer.data['related_tables'][0]['field_mapping'], {"source": "target"})
        self.assertEqual(serializer.data['related_tables'][0]['related_table_title'], "Custom title")
        self.assertEqual(serializer.data['related_tables'][0]['ordering'], 1)

    def test_to_dict_serializes_related_tables_by_relation_order(self):
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
        TableToTable.objects.create(from_table=self.table, to_table=first_table, field_mapping={}, ordering=2)
        TableToTable.objects.create(from_table=self.table, to_table=second_table, field_mapping={}, ordering=1)

        data = self.table.to_dict(request=self.get_request())

        self.assertEqual(
            [relation['to_table']['title'] for relation in data['related_tables']],
            ['A Table', 'Z Table'],
        )

    def test_related_tables_updates_ordering(self):
        related_table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        relation = TableToTable.objects.create(
            from_table=self.table,
            to_table=related_table,
            field_mapping={},
            ordering=5,
        )
        serializer = TableSerializer(
            instance=self.table,
            data={
                'related_tables': [{
                    'id': relation.id,
                    'to_table': related_table.id,
                    'field_mapping': {},
                    'ordering': 0,
                }]
            },
            partial=True,
            context={'request': self.get_request()},
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        relation.refresh_from_db()
        self.assertEqual(relation.ordering, 0)

    def test_empty_related_tables_removes_relations(self):
        related_table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        TableToTable.objects.create(from_table=self.table, to_table=related_table, field_mapping={})
        serializer = TableSerializer(
            instance=self.table,
            data={'related_tables': []},
            partial=True,
            context={'request': self.get_request()},
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        self.assertFalse(TableToTable.objects.filter(from_table=self.table).exists())

    def test_patch_without_related_tables_keeps_existing_relations(self):
        related_table = Table.objects.create(
            title='Related table',
            slug='related-table',
            source=self.source,
            layer_name='related:table',
        )
        relation = TableToTable.objects.create(from_table=self.table, to_table=related_table, field_mapping={})
        serializer = TableSerializer(
            instance=self.table,
            data={'title': 'Updated table'},
            partial=True,
            context={'request': self.get_request()},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertTrue(TableToTable.objects.filter(id=relation.id).exists())

    def test_related_tables_update_keeps_adds_and_removes_relations(self):
        kept_table = Table.objects.create(
            title='Kept table', slug='kept-table', source=self.source, layer_name='kept:table'
        )
        removed_table = Table.objects.create(
            title='Removed table', slug='removed-table', source=self.source, layer_name='removed:table'
        )
        added_table = Table.objects.create(
            title='Added table', slug='added-table', source=self.source, layer_name='added:table'
        )
        kept_relation = TableToTable.objects.create(from_table=self.table, to_table=kept_table, field_mapping={})
        removed_relation = TableToTable.objects.create(from_table=self.table, to_table=removed_table, field_mapping={})
        serializer = TableSerializer(
            instance=self.table,
            data={
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
            },
            partial=True,
            context={'request': self.get_request()},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        kept_relation.refresh_from_db()
        self.assertEqual(kept_relation.field_mapping, {'old': 'new'})
        self.assertEqual(kept_relation.related_table_title, 'Kept title')
        self.assertEqual(kept_relation.ordering, 1)
        self.assertFalse(TableToTable.objects.filter(id=removed_relation.id).exists())
        self.assertTrue(TableToTable.objects.filter(from_table=self.table, to_table=added_table).exists())
