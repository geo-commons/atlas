from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from webservice.models import Map, MapLayer, MapCategory, Layer, Category, Source
from webservice.serializers import MapSerializer, MapLayerSerializer, MapCategorySerializer


class MapLayerSerializerTest(APITestCase):
    """Test MapLayerSerializer"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.source = Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com'
        )
        self.category = Category.objects.create(
            slug='test-cat',
            title='Test Category',
            ordering=1
        )
        self.layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=self.source,
            layer_type=self.category
        )

    def test_map_layer_serialization(self):
        """Test MapLayerSerializer correctly serializes data"""
        map_instance = Map.objects.create(title='Test Map', slug='test-map')
        map_layer = MapLayer.objects.create(
            map=map_instance,
            layer=self.layer,
            settings={'opacity': 0.8},
            ordering=1
        )

        serializer = MapLayerSerializer(map_layer)
        data = serializer.data

        self.assertEqual(data['layer'], self.layer.id)
        self.assertEqual(data['settings'], {'opacity': 0.8})
        self.assertEqual(data['ordering'], 1)
        self.assertIsNone(data['map_category'])

    def test_map_layer_serialization_with_category(self):
        """Test MapLayerSerializer with map_category"""
        map_instance = Map.objects.create(title='Test Map', slug='test-map')
        map_category = MapCategory.objects.create(
            map=map_instance,
            category=self.category,
            ordering=1
        )
        map_layer = MapLayer.objects.create(
            map=map_instance,
            layer=self.layer,
            settings={'visible': True},
            ordering=0,
            map_category=map_category
        )

        serializer = MapLayerSerializer(map_layer)
        data = serializer.data

        self.assertEqual(data['map_category'], map_category.id)


class MapCategorySerializerTest(APITestCase):
    """Test MapCategorySerializer"""

    def setUp(self):
        self.category = Category.objects.create(
            slug='test-cat',
            title='Test Category',
            ordering=1
        )

    def test_map_category_serialization(self):
        """Test MapCategorySerializer correctly serializes data"""
        map_instance = Map.objects.create(title='Test Map', slug='test-map')
        map_category = MapCategory.objects.create(
            map=map_instance,
            category=self.category,
            ordering=2
        )

        serializer = MapCategorySerializer(map_category)
        data = serializer.data

        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['ordering'], 2)


class MapSerializerTest(APITestCase):
    """Test MapSerializer create/update operations"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.source = Source.objects.create(
            slug='test-source',
            title='Test Source',
            url='http://test.com'
        )
        self.category1 = Category.objects.create(
            slug='cat-1',
            title='Category 1',
            ordering=1
        )
        self.category2 = Category.objects.create(
            slug='cat-2',
            title='Category 2',
            ordering=2
        )
        self.layer1 = Layer.objects.create(
            slug='layer-1',
            title='Layer 1',
            layer_source=self.source,
            layer_type=self.category1
        )
        self.layer2 = Layer.objects.create(
            slug='layer-2',
            title='Layer 2',
            layer_source=self.source,
            layer_type=self.category2
        )

    def test_create_map_with_layers_and_categories(self):
        """Test MapSerializer creates map with nested layers and categories"""
        data = {
            'title': 'New Map',
            'slug': 'new-map',
            'published': True,
            'show_in_overview': True,
            'categories': [
                {'category': self.category1.id, 'ordering': 0},
                {'category': self.category2.id, 'ordering': 1}
            ],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {'opacity': 0.8},
                    'ordering': 0,
                    'map_category': None
                },
                {
                    'layer': self.layer2.id,
                    'settings': {'visible': True},
                    'ordering': 1,
                    'map_category': None
                }
            ]
        }

        serializer = MapSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        map_instance = serializer.save()

        self.assertEqual(map_instance.title, 'New Map')
        self.assertEqual(map_instance.slug, 'new-map')

        self.assertEqual(map_instance.map_categories.count(), 2)

        self.assertEqual(map_instance.map_layers.count(), 2)

    def test_create_map_with_position_settings(self):
        data = {
            'title': 'Map With Position',
            'slug': 'map-with-position',
            'settings': {
                'position': {
                    'zoom': 9,
                    'center': {
                        'x': 123,
                        'y': 456,
                    },
                },
            },
            'categories': [],
            'layers': [],
        }

        serializer = MapSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        map_instance = serializer.save()

        self.assertEqual(
            map_instance.settings['position'],
            {
                'zoom': 9,
                'center': {
                    'x': 123,
                    'y': 456,
                },
            },
        )

    def test_create_map_with_layer_category_references(self):
        """Test MapSerializer creates map where layers reference categories"""
        data = {
            'title': 'New Map',
            'slug': 'new-map',
            'published': True,
            'show_in_overview': True,
            'categories': [
                {'category': self.category1.id, 'ordering': 0},
            ],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {},
                    'ordering': 0,
                }
            ]
        }

        serializer = MapSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        map_instance = serializer.save()

        map_layer = map_instance.map_layers.first()
        self.assertIsNotNone(map_layer.map_category)
        self.assertEqual(map_layer.map_category.category, self.category1)

    def test_update_map_legacy_categories_creates_parent_for_subcategory(self):
        parent_category = Category.objects.create(slug='parent-category', title='Parent category', ordering=3)
        subcategory = Category.objects.create(
            slug='subcategory',
            title='Subcategory',
            ordering=4,
            parent=parent_category,
        )
        layer = Layer.objects.create(
            slug='subcategory-layer',
            title='Subcategory layer',
            layer_source=self.source,
            layer_type=subcategory,
        )
        map_instance = Map.objects.create(title='Existing Map', slug='existing-map')
        data = {
            'title': 'Existing Map',
            'slug': 'existing-map',
            'categories': [
                {'category': subcategory.id, 'ordering': 0},
            ],
            'layers': [
                {
                    'layer': layer.id,
                    'settings': {},
                    'ordering': 0,
                }
            ],
        }

        serializer = MapSerializer(map_instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_map = serializer.save()

        parent_map_category = updated_map.map_categories.get(category=parent_category)
        subcategory_map_category = updated_map.map_categories.get(category=subcategory)
        map_layer = updated_map.map_layers.get(layer=layer)
        self.assertEqual(parent_map_category.ordering, parent_category.ordering)
        self.assertEqual(map_layer.map_category, subcategory_map_category)

    def test_update_map_adds_new_layers_and_categories(self):
        """Test MapSerializer update adds new layers and categories"""
        map_instance = Map.objects.create(
            title='Existing Map',
            slug='existing-map',
            published=True
        )

        data = {
            'title': 'Updated Map',
            'slug': 'existing-map',
            'published': True,
            'show_in_overview': False,
            'categories': [
                {'category': self.category1.id, 'ordering': 5}
            ],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {'new': True},
                    'ordering': 3,
                    'map_category': None
                }
            ]
        }

        serializer = MapSerializer(map_instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_map = serializer.save()

        self.assertEqual(updated_map.title, 'Updated Map')
        self.assertFalse(updated_map.show_in_overview)

        self.assertEqual(updated_map.map_categories.count(), 1)
        map_category = updated_map.map_categories.first()
        self.assertEqual(map_category.ordering, 5)

        self.assertEqual(updated_map.map_layers.count(), 1)
        map_layer = updated_map.map_layers.first()
        self.assertEqual(map_layer.settings, {'new': True})
        self.assertEqual(map_layer.ordering, 3)
        self.assertEqual(map_layer.map_category, map_category)

    def test_update_map_removes_deleted_layers_and_categories(self):
        """Test MapSerializer update removes layers/categories not in request"""
        map_instance = Map.objects.create(
            title='Existing Map',
            slug='existing-map'
        )

        map_category1 = MapCategory.objects.create(
            map=map_instance,
            category=self.category1,
            ordering=1
        )
        map_category2 = MapCategory.objects.create(
            map=map_instance,
            category=self.category2,
            ordering=2
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=self.layer1,
            settings={},
            ordering=1,
            map_category=map_category1
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=self.layer2,
            settings={},
            ordering=2,
            map_category=map_category2
        )

        data = {
            'title': 'Existing Map',
            'slug': 'existing-map',
            'categories': [
                {'category': self.category1.id, 'ordering': 1}
            ],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {'updated': True},
                    'ordering': 1,
                    'map_category': None
                }
            ]
        }

        serializer = MapSerializer(map_instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_map = serializer.save()

        self.assertEqual(updated_map.map_categories.count(), 1)
        self.assertIsNotNone(updated_map.map_categories.filter(category=self.category1).first())
        self.assertIsNone(updated_map.map_categories.filter(category=self.category2).first())

        self.assertEqual(updated_map.map_layers.count(), 1)
        self.assertIsNotNone(updated_map.map_layers.filter(layer=self.layer1).first())

    def test_update_map_updates_existing_layers_and_categories(self):
        """Test MapSerializer update updates existing layers and categories"""
        map_instance = Map.objects.create(
            title='Existing Map',
            slug='existing-map'
        )

        map_category = MapCategory.objects.create(
            map=map_instance,
            category=self.category1,
            ordering=1
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=self.layer1,
            settings={'old': True},
            ordering=1,
            map_category=map_category
        )

        data = {
            'title': 'Existing Map',
            'slug': 'existing-map',
            'categories': [
                {'category': self.category1.id, 'ordering': 10}
            ],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {'new': True},
                    'ordering': 20,
                    'map_category': map_category.id
                }
            ]
        }

        serializer = MapSerializer(map_instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_map = serializer.save()

        map_category.refresh_from_db()
        self.assertEqual(map_category.ordering, 10)

        map_layer = updated_map.map_layers.first()
        self.assertEqual(map_layer.settings, {'new': True})
        self.assertEqual(map_layer.ordering, 20)

    def test_update_map_rejects_map_category_from_other_map(self):
        """Test map_category validation rejects categories that belong to another map."""
        map_instance = Map.objects.create(
            title='Map A',
            slug='map-a'
        )
        other_map = Map.objects.create(
            title='Map B',
            slug='map-b'
        )
        other_map_category = MapCategory.objects.create(
            map=other_map,
            category=self.category1,
            ordering=0
        )

        data = {
            'title': 'Map A',
            'slug': 'map-a',
            'categories': [],
            'layers': [
                {
                    'layer': self.layer1.id,
                    'settings': {'new': True},
                    'ordering': 1,
                    'map_category': other_map_category.id,
                }
            ]
        }

        serializer = MapSerializer(map_instance, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('layers', serializer.errors)

    def test_serialize_map_with_nested_data(self):
        """Test MapSerializer correctly serializes map with layers and categories"""
        map_instance = Map.objects.create(
            title='Test Map',
            slug='test-map',
            published=True,
            show_in_overview=True
        )

        map_category = MapCategory.objects.create(
            map=map_instance,
            category=self.category1,
            ordering=1
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=self.layer1,
            settings={'test': True},
            ordering=0,
            map_category=map_category
        )

        serializer = MapSerializer(map_instance)
        data = serializer.data

        self.assertEqual(data['title'], 'Test Map')
        self.assertEqual(data['slug'], 'test-map')
        self.assertEqual(len(data['layers']), 1)
        self.assertEqual(len(data['categories']), 1)
        self.assertEqual(data['layers'][0]['layer'], self.layer1.id)
        self.assertEqual(data['layers'][0]['settings'], {'test': True})
        self.assertEqual(data['categories'][0]['category'], self.category1.id)

    def test_serialize_map_detail_includes_flat_layers_and_categories(self):
        parent_category = Category.objects.create(
            slug='infrastructure',
            title='Infrastructure',
            ordering=30,
        )
        subcategory = Category.objects.create(
            slug='roads',
            title='Roads',
            ordering=20,
            parent=parent_category,
        )
        direct_layer = Layer.objects.create(
            slug='public-lights',
            title='Public lights',
            layer_name='atlas:public_lights',
            layer_source=self.source,
            layer_type=parent_category,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        subcategory_layer = Layer.objects.create(
            slug='traffic-incidents',
            title='Traffic incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=subcategory,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        map_instance = Map.objects.create(title='Test Map', slug='test-map')
        parent_map_category = MapCategory.objects.create(map=map_instance, category=parent_category, ordering=3)
        subcategory_map_category = MapCategory.objects.create(map=map_instance, category=subcategory, ordering=1)
        MapLayer.objects.create(
            map=map_instance,
            layer=direct_layer,
            map_category=parent_map_category,
            ordering=2,
            settings={},
        )
        MapLayer.objects.create(
            map=map_instance,
            layer=subcategory_layer,
            map_category=subcategory_map_category,
            ordering=1,
            settings={
                'customSettings': True,
                'opacity': 0.5,
            },
        )
        request = self.factory.get('/atlas/api/v1/maps/test-map/')
        request.user = AnonymousUser()

        serializer = MapSerializer(map_instance, context={'request': request})
        data = serializer.data

        self.assertEqual(
            data['categories'],
            [
                {'id': subcategory_map_category.id, 'category': subcategory.id, 'title': subcategory.title, 'ordering': 1},
                {'id': parent_map_category.id, 'category': parent_category.id, 'title': parent_category.title, 'ordering': 3},
            ],
        )
        self.assertEqual([layer['layer'] for layer in data['layers']], [subcategory_layer.id, direct_layer.id])
        self.assertEqual(data['layers'][0]['settings'], {'customSettings': True, 'opacity': 0.5})

    def test_serialize_map_list_does_not_crash(self):
        """Test MapSerializer(many=True) works for map list endpoints."""
        map1 = Map.objects.create(title='Map 1', slug='map-1')
        map2 = Map.objects.create(title='Map 2', slug='map-2')

        serializer = MapSerializer([map1, map2], many=True)
        data = serializer.data

        self.assertEqual(len(data), 2)