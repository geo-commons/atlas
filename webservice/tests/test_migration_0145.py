from django.test import TransactionTestCase
from django.apps import apps


class Migration0145Test(TransactionTestCase):
    """Test the create_map_categories data migration from migration 0145"""

    def setUp(self):
        # Get models using the apps registry (mimicking migration context)
        self.Map = apps.get_model('webservice', 'Map')
        self.Layer = apps.get_model('webservice', 'Layer')
        self.Category = apps.get_model('webservice', 'Category')
        self.Source = apps.get_model('webservice', 'Source')
        self.MapLayer = apps.get_model('webservice', 'MapLayer')
        self.MapCategory = apps.get_model('webservice', 'MapCategory')
        
        self.source = self.Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com'
        )

    def test_create_map_categories_creates_categories(self):
        """Test that migration creates MapCategory records for each unique category"""
        category1 = self.Category.objects.create(
            slug='cat1',
            title='Category 1',
            ordering=1
        )
        category2 = self.Category.objects.create(
            slug='cat2',
            title='Category 2',
            ordering=2
        )

        layer1 = self.Layer.objects.create(
            slug='layer1',
            title='Layer 1',
            layer_source=self.source,
            layer_type=category1,
            ordering=1
        )
        layer2 = self.Layer.objects.create(
            slug='layer2',
            title='Layer 2',
            layer_source=self.source,
            layer_type=category1,
            ordering=2
        )
        layer3 = self.Layer.objects.create(
            slug='layer3',
            title='Layer 3',
            layer_source=self.source,
            layer_type=category2,
            ordering=1
        )

        map_instance = self.Map.objects.create(
            title='Test Map',
            slug='test-map'
        )
        self.MapLayer.objects.create(map=map_instance, layer=layer1, settings={})
        self.MapLayer.objects.create(map=map_instance, layer=layer2, settings={})
        self.MapLayer.objects.create(map=map_instance, layer=layer3, settings={})

        # Import and run the migration function
        from webservice.migrations._0145_create_map_categories import create_map_categories
        create_map_categories(apps, None)

        map_categories = self.MapCategory.objects.filter(map=map_instance)
        self.assertEqual(map_categories.count(), 2)

        cat1_mapcat = map_categories.get(category=category1)
        cat2_mapcat = map_categories.get(category=category2)
        self.assertEqual(cat1_mapcat.ordering, 0)
        self.assertEqual(cat2_mapcat.ordering, 1)

    def test_create_map_categories_associates_layers(self):
        """Test that migration associates MapLayers with their MapCategory"""
        category = self.Category.objects.create(
            slug='cat1',
            title='Category 1',
            ordering=1
        )

        layer1 = self.Layer.objects.create(
            slug='layer1',
            title='Layer 1',
            layer_source=self.source,
            layer_type=category,
            ordering=1
        )
        layer2 = self.Layer.objects.create(
            slug='layer2',
            title='Layer 2',
            layer_source=self.source,
            layer_type=category,
            ordering=2
        )

        map_instance = self.Map.objects.create(
            title='Test Map',
            slug='test-map'
        )
        map_layer1 = self.MapLayer.objects.create(map=map_instance, layer=layer1, settings={})
        map_layer2 = self.MapLayer.objects.create(map=map_instance, layer=layer2, settings={})

        from webservice.migrations._0145_create_map_categories import create_map_categories
        create_map_categories(apps, None)

        map_layer1.refresh_from_db()
        map_layer2.refresh_from_db()

        map_category = self.MapCategory.objects.get(map=map_instance)
        self.assertEqual(map_layer1.map_category, map_category)
        self.assertEqual(map_layer2.map_category, map_category)

        self.assertEqual(map_layer1.ordering, 0)
        self.assertEqual(map_layer2.ordering, 1)

    def test_create_map_categories_skips_layers_without_type(self):
        """Test that migration handles layers without a layer_type"""
        category = self.Category.objects.create(
            slug='cat1',
            title='Category 1',
            ordering=1
        )

        layer_with_type = self.Layer.objects.create(
            slug='layer1',
            title='Layer With Type',
            layer_source=self.source,
            layer_type=category,
            ordering=1
        )
        layer_without_type = self.Layer.objects.create(
            slug='layer2',
            title='Layer Without Type',
            layer_source=self.source,
            layer_type=None,
            ordering=2
        )

        map_instance = self.Map.objects.create(
            title='Test Map',
            slug='test-map'
        )
        self.MapLayer.objects.create(map=map_instance, layer=layer_with_type, settings={})
        self.MapLayer.objects.create(map=map_instance, layer=layer_without_type, settings={})

        from webservice.migrations._0145_create_map_categories import create_map_categories
        create_map_categories(apps, None)

        map_categories = self.MapCategory.objects.filter(map=map_instance)
        self.assertEqual(map_categories.count(), 1)

        map_layer_without_type = self.MapLayer.objects.get(layer=layer_without_type)
        self.assertIsNone(map_layer_without_type.map_category)

    def test_create_map_categories_multiple_maps(self):
        """Test that migration handles multiple maps independently"""
        category1 = self.Category.objects.create(
            slug='cat1',
            title='Category 1',
            ordering=1
        )
        category2 = self.Category.objects.create(
            slug='cat2',
            title='Category 2',
            ordering=2
        )

        layer1 = self.Layer.objects.create(
            slug='layer1',
            title='Layer 1',
            layer_source=self.source,
            layer_type=category1,
            ordering=1
        )
        layer2 = self.Layer.objects.create(
            slug='layer2',
            title='Layer 2',
            layer_source=self.source,
            layer_type=category2,
            ordering=1
        )

        map1 = self.Map.objects.create(title='Map 1', slug='map1')
        map2 = self.Map.objects.create(title='Map 2', slug='map2')

        self.MapLayer.objects.create(map=map1, layer=layer1, settings={})
        self.MapLayer.objects.create(map=map1, layer=layer2, settings={})

        self.MapLayer.objects.create(map=map2, layer=layer2, settings={})

        from webservice.migrations._0145_create_map_categories import create_map_categories
        create_map_categories(apps, None)

        self.assertEqual(self.MapCategory.objects.filter(map=map1).count(), 2)
        self.assertEqual(self.MapCategory.objects.filter(map=map2).count(), 1)

    def test_create_map_categories_empty_map(self):
        """Test that migration handles maps without layers"""
        map_instance = self.Map.objects.create(
            title='Empty Map',
            slug='empty-map'
        )

        from webservice.migrations._0145_create_map_categories import create_map_categories
        create_map_categories(apps, None)

        map_categories = self.MapCategory.objects.filter(map=map_instance)
        self.assertEqual(map_categories.count(), 0)
