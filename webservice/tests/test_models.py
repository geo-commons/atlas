from django.test import TestCase

from webservice.models import Category, Layer, Map, MapCategory, MapLayer, Source


class CategoryModelTest(TestCase):
    def test_changing_parent_creates_missing_parent_map_categories(self):
        parent_category = Category.objects.create(
            title='Public space',
            slug='public-space',
            ordering=7,
        )
        subcategory = Category.objects.create(
            title='Signs',
            slug='signs',
        )
        map_instance = Map.objects.create(title='Test Map', slug='test-map')

        MapCategory.objects.create(map=map_instance, category=subcategory, ordering=3)

        subcategory.parent = parent_category
        subcategory.save()

        parent_map_category = MapCategory.objects.get(map=map_instance, category=parent_category)
        self.assertEqual(parent_map_category.ordering, parent_category.ordering)

    def test_removing_parent_deletes_unused_parent_map_category(self):
        parent_category = Category.objects.create(title='Public space', slug='public-space')
        subcategory = Category.objects.create(title='Signs', slug='signs', parent=parent_category)
        map_instance = Map.objects.create(title='Test Map', slug='test-map')

        MapCategory.objects.create(map=map_instance, category=parent_category)
        MapCategory.objects.create(map=map_instance, category=subcategory)

        subcategory.parent = None
        subcategory.save()

        self.assertFalse(MapCategory.objects.filter(map=map_instance, category=parent_category).exists())
        self.assertTrue(MapCategory.objects.filter(map=map_instance, category=subcategory).exists())

    def test_changing_parent_deletes_unused_previous_parent_map_category(self):
        previous_parent = Category.objects.create(title='Public space', slug='public-space')
        next_parent = Category.objects.create(title='Infrastructure', slug='infrastructure')
        subcategory = Category.objects.create(title='Signs', slug='signs', parent=previous_parent)
        map_instance = Map.objects.create(title='Test Map', slug='test-map')

        MapCategory.objects.create(map=map_instance, category=previous_parent)
        MapCategory.objects.create(map=map_instance, category=subcategory)

        subcategory.parent = next_parent
        subcategory.save()

        self.assertFalse(MapCategory.objects.filter(map=map_instance, category=previous_parent).exists())
        self.assertTrue(MapCategory.objects.filter(map=map_instance, category=next_parent).exists())
        self.assertTrue(MapCategory.objects.filter(map=map_instance, category=subcategory).exists())


class LayerModelTest(TestCase):
    def test_changing_layer_category_updates_existing_map_layers(self):
        source = Source.objects.create(title='Source', slug='source', url='https://example.com')
        previous_category = Category.objects.create(title='Previous', slug='previous')
        next_parent = Category.objects.create(title='Next parent', slug='next-parent')
        next_subcategory = Category.objects.create(title='Next child', slug='next-child', parent=next_parent)
        layer = Layer.objects.create(
            title='Layer',
            slug='layer',
            layer_name='atlas:layer',
            layer_source=source,
            layer_type=previous_category,
        )
        map_instance = Map.objects.create(title='Test Map', slug='test-map')
        previous_map_category = MapCategory.objects.create(map=map_instance, category=previous_category)
        map_layer = MapLayer.objects.create(
            map=map_instance,
            layer=layer,
            map_category=previous_map_category,
            settings={},
        )

        layer.layer_type = next_subcategory
        layer.save()

        map_layer.refresh_from_db()
        next_map_category = MapCategory.objects.get(map=map_instance, category=next_subcategory)
        self.assertEqual(map_layer.map_category, next_map_category)
        self.assertTrue(MapCategory.objects.filter(map=map_instance, category=next_parent).exists())
        self.assertFalse(MapCategory.objects.filter(map=map_instance, category=previous_category).exists())
