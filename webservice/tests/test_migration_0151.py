import importlib

from django.apps import apps
from django.test import TransactionTestCase

create_main_map = importlib.import_module('webservice.migrations.0151_map_is_main').create_main_map


class Migration0151Test(TransactionTestCase):
    def setUp(self):
        self.Map = apps.get_model('webservice', 'Map')
        self.Layer = apps.get_model('webservice', 'Layer')
        self.Source = apps.get_model('webservice', 'Source')
        self.Category = apps.get_model('webservice', 'Category')
        self.MapLayer = apps.get_model('webservice', 'MapLayer')
        self.MapCategory = apps.get_model('webservice', 'MapCategory')

        self.source = self.Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com',
        )

    def test_create_main_map_creates_categories_for_layer_types(self):
        category_a = self.Category.objects.create(slug='cat-a', title='Category A', ordering=1)
        category_b = self.Category.objects.create(slug='cat-b', title='Category B', ordering=2)

        layer_a = self.Layer.objects.create(
            slug='layer-a',
            title='Layer A',
            layer_source=self.source,
            layer_type=category_a,
            published=True,
        )
        layer_b = self.Layer.objects.create(
            slug='layer-b',
            title='Layer B',
            layer_source=self.source,
            layer_type=category_b,
            published=True,
        )

        create_main_map(apps, None)

        main_map = self.Map.objects.get(is_main=True)
        map_categories = list(self.MapCategory.objects.filter(map=main_map).order_by('ordering'))
        map_layers = list(self.MapLayer.objects.filter(map=main_map).order_by('ordering'))

        self.assertEqual(len(map_categories), 2)
        self.assertEqual(map_categories[0].category_id, category_a.id)
        self.assertEqual(map_categories[1].category_id, category_b.id)
        self.assertEqual(map_layers[0].layer_id, layer_a.id)
        self.assertEqual(map_layers[0].map_category_id, map_categories[0].id)
        self.assertEqual(map_layers[1].layer_id, layer_b.id)
        self.assertEqual(map_layers[1].map_category_id, map_categories[1].id)

    def test_create_main_map_keeps_layers_without_type_uncategorized(self):
        self.Layer.objects.create(
            slug='layer-a',
            title='Layer A',
            layer_source=self.source,
            layer_type=None,
            published=True,
        )

        create_main_map(apps, None)

        main_map = self.Map.objects.get(is_main=True)
        self.assertEqual(self.MapCategory.objects.filter(map=main_map).count(), 0)
        self.assertIsNone(self.MapLayer.objects.get(map=main_map).map_category)
