from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from webservice.models import Category, Layer, Map, MapLayer, Source
from webservice.serializers import LayerCreateUpdateSerializer, LayerSerializer


class LayerSerializerTest(APITestCase):
    def test_serializes_assigned_maps(self):
        source = Source.objects.create(slug='test-source', title='Test Source', url='http://test.com')
        category = Category.objects.create(slug='test-category', title='Test Category')
        layer = Layer.objects.create(
            slug='test-layer',
            title='Test Layer',
            layer_source=source,
            layer_type=category,
        )
        map_instance = Map.objects.create(title='Map 1', slug='map-1')
        MapLayer.objects.create(map=map_instance, layer=layer, settings={})
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()

        serializer = LayerSerializer(instance=layer, context={'request': request})

        self.assertEqual(serializer.data['assigned_maps'], [map_instance.id])


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
