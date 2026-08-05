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

    def test_sync_map_assignments_adds_layer_to_multiple_maps_with_categories(self):
        source = Source.objects.create(title='Source', slug='source', url='https://example.com')
        parent_category = Category.objects.create(title='Parent', slug='parent', ordering=4)
        subcategory = Category.objects.create(
            title='Subcategory',
            slug='subcategory',
            parent=parent_category,
            ordering=2,
        )
        layer = Layer.objects.create(title='Layer', slug='layer', layer_source=source, layer_type=subcategory)
        map1 = Map.objects.create(title='Map 1', slug='map-1')
        map2 = Map.objects.create(title='Map 2', slug='map-2')

        layer.sync_map_assignments([map1, map2])

        for map_instance in [map1, map2]:
            with self.subTest(map=map_instance.slug):
                parent_map_category = MapCategory.objects.get(map=map_instance, category=parent_category)
                subcategory_map_category = MapCategory.objects.get(map=map_instance, category=subcategory)
                map_layer = MapLayer.objects.get(map=map_instance, layer=layer)

                self.assertEqual(parent_map_category.ordering, parent_category.ordering)
                self.assertEqual(subcategory_map_category.ordering, subcategory.ordering)
                self.assertEqual(map_layer.map_category, subcategory_map_category)
                self.assertEqual(map_layer.settings, {'customSettings': False})
                self.assertEqual(map_layer.ordering, 0)

    def test_sync_map_assignments_removes_layer_and_unused_categories(self):
        source = Source.objects.create(title='Source', slug='source', url='https://example.com')
        parent_category = Category.objects.create(title='Parent', slug='parent')
        subcategory = Category.objects.create(title='Subcategory', slug='subcategory', parent=parent_category)
        layer = Layer.objects.create(title='Layer', slug='layer', layer_source=source, layer_type=subcategory)
        map1 = Map.objects.create(title='Map 1', slug='map-1')
        map2 = Map.objects.create(title='Map 2', slug='map-2')

        layer.sync_map_assignments([map1, map2])
        layer.sync_map_assignments([map2])

        self.assertFalse(MapLayer.objects.filter(map=map1, layer=layer).exists())
        self.assertFalse(MapCategory.objects.filter(map=map1, category=subcategory).exists())
        self.assertFalse(MapCategory.objects.filter(map=map1, category=parent_category).exists())
        self.assertTrue(MapLayer.objects.filter(map=map2, layer=layer).exists())
        self.assertTrue(MapCategory.objects.filter(map=map2, category=subcategory).exists())
        self.assertTrue(MapCategory.objects.filter(map=map2, category=parent_category).exists())

    def test_sync_map_assignments_keeps_category_when_other_layer_still_uses_it(self):
        source = Source.objects.create(title='Source', slug='source', url='https://example.com')
        parent_category = Category.objects.create(title='Parent', slug='parent')
        subcategory = Category.objects.create(title='Subcategory', slug='subcategory', parent=parent_category)
        layer = Layer.objects.create(title='Layer', slug='layer', layer_source=source, layer_type=subcategory)
        other_layer = Layer.objects.create(
            title='Other Layer',
            slug='other-layer',
            layer_source=source,
            layer_type=subcategory,
        )
        map_instance = Map.objects.create(title='Map', slug='map')
        parent_map_category = MapCategory.objects.create(map=map_instance, category=parent_category)
        subcategory_map_category = MapCategory.objects.create(map=map_instance, category=subcategory)
        MapLayer.objects.create(
            map=map_instance,
            layer=layer,
            map_category=subcategory_map_category,
            settings={},
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=other_layer,
            map_category=subcategory_map_category,
            settings={},
        )

        layer.sync_map_assignments([])

        self.assertFalse(MapLayer.objects.filter(map=map_instance, layer=layer).exists())
        self.assertTrue(MapCategory.objects.filter(pk=parent_map_category.pk).exists())
        self.assertTrue(MapCategory.objects.filter(pk=subcategory_map_category.pk).exists())

    def test_sync_map_assignments_preserves_existing_layer_settings(self):
        source = Source.objects.create(title='Source', slug='source', url='https://example.com')
        category = Category.objects.create(title='Category', slug='category')
        layer = Layer.objects.create(title='Layer', slug='layer', layer_source=source, layer_type=category)
        map_instance = Map.objects.create(title='Map', slug='map')
        map_category = MapCategory.objects.create(map=map_instance, category=category)
        MapLayer.objects.create(
            map=map_instance,
            layer=layer,
            map_category=map_category,
            settings={'customSettings': True, 'is_visible': True},
            ordering=7,
        )

        layer.sync_map_assignments([map_instance])

        map_layer = MapLayer.objects.get(map=map_instance, layer=layer)
        self.assertEqual(map_layer.settings, {'customSettings': True, 'is_visible': True})
        self.assertEqual(map_layer.ordering, 7)
