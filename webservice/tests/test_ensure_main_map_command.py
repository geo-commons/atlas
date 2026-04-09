from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from webservice.models import Category, Layer, Map, MapCategory, MapLayer, Source


class EnsureMainMapCommandTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com',
        )

    def test_command_creates_main_map_with_published_layers_and_categories(self):
        Map.objects.filter(is_main=True).delete()

        category_a = Category.objects.create(slug='cat-a', title='Category A', ordering=1)
        category_b = Category.objects.create(slug='cat-b', title='Category B', ordering=2)

        published_layer = Layer.objects.create(
            slug='layer-a',
            title='Layer A',
            layer_source=self.source,
            layer_type=category_a,
            published=True,
            ordering=1,
        )
        Layer.objects.create(
            slug='layer-b',
            title='Layer B',
            layer_source=self.source,
            layer_type=category_b,
            published=False,
            ordering=2,
        )

        stdout = StringIO()
        call_command('ensure_main_map', stdout=stdout)

        main_map = Map.objects.get(is_main=True)

        self.assertEqual(Map.objects.filter(is_main=True).count(), 1)
        self.assertTrue(main_map.published)
        self.assertFalse(main_map.show_in_overview)
        self.assertEqual(main_map.title, 'Hoofdkaart')
        self.assertEqual(MapCategory.objects.filter(map=main_map).count(), 1)
        self.assertEqual(MapLayer.objects.filter(map=main_map).count(), 1)
        self.assertEqual(MapLayer.objects.get(map=main_map).layer_id, published_layer.id)
        self.assertIn('Created main map', stdout.getvalue())

    def test_command_is_idempotent_and_repairs_existing_main_map_flags(self):
        main_map = Map.objects.get(is_main=True)
        main_map.title = 'Existing Main'
        main_map.slug = 'existing-main'
        main_map.features = {}
        main_map.settings = {}
        main_map.published = False
        main_map.show_in_overview = True
        main_map.save()

        stdout = StringIO()
        call_command('ensure_main_map', stdout=stdout)

        main_map.refresh_from_db()

        self.assertEqual(Map.objects.filter(is_main=True).count(), 1)
        self.assertTrue(main_map.published)
        self.assertFalse(main_map.show_in_overview)
        self.assertEqual(MapLayer.objects.filter(map=main_map).count(), 0)
        self.assertIn('Main map already exists', stdout.getvalue())
