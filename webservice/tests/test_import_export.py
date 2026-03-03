import json

from django.test import TestCase

from webservice.models import Layer, MapLayer, Map, Category, MapCategory
from webservice.resources import MapResource


class ImportExportMapTest(TestCase):
    def setUp(self):
        self.layer1 = Layer.objects.create(
            slug='topografische-kaart-grijs',
            title='Topografische Kaart Grijs'
        )

        self.layer2 = Layer.objects.create(
            slug='id_beheer_afvalbakken',
            title='Beheer Afvalbakken'
        )

        self.category1 = Category.objects.create(
            slug='beheer',
            title='Beheer'
        )

        self.category2 = Category.objects.create(
            slug='groen',
            title='Groen'
        )

        self.map = Map.objects.create(
            title='afvalbakken',
            slug='afvalbakken',
            published=False,
            show_in_overview=True
        )

        self.layer_data = 'topografische-kaart-grijs::{"customSettings": false}::0::no-category|id_beheer_afvalbakken::{"id": 52, "slug": "id_beheer_afvalbakken", "title": "Beheer Afvalbakken", "customSettings": true}::1::no-category'

        self.category_data = "beheer::1|groen::2"

        self.resource = MapResource()

    def test_export_layers(self):
        """Test the export (dehydrate) method processes layer data correctly"""
        MapLayer.objects.create(
            map=self.map,
            layer=self.layer1,
            settings={"customSettings": False}
        )
        MapLayer.objects.create(
            map=self.map,
            layer=self.layer2,
            settings={
                "id": 52,
                "slug": "id_beheer_afvalbakken",
                "title": "Beheer Afvalbakken",
                "customSettings": True
            }
        )

        result = self.resource.dehydrate_layers(self.map)

        self.assertIn('topografische-kaart-grijs', result)
        self.assertIn('id_beheer_afvalbakken', result)

        layers_data = result.split("|")
        self.assertEqual(len(layers_data), 2)

        for layer_string in layers_data:
            parts = layer_string.split('::')
            slug = parts[0]
            settings = json.loads(parts[1])
            ordering = int(parts[2])

            if slug == 'topografische-kaart-grijs':
                self.assertEqual(settings, {"customSettings": False})
                self.assertEqual(ordering, 0)
            elif slug == 'id_beheer_afvalbakken':
                self.assertTrue('customSettings' in settings)
                self.assertEqual(ordering, 0)

    def test_export_empty_layers(self):
        """Test export with no layers"""
        result = self.resource.dehydrate_layers(self.map)
        self.assertEqual(result, '')

    def test_import_layers(self):
        """Test the import (after_save_instance) method creates MapLayer instances"""
        row = {'slug': self.map.slug, 'layers': self.layer_data}

        self.resource.after_save_instance(self.map, row)

        map_layers = MapLayer.objects.filter(map=self.map)
        self.assertEqual(map_layers.count(), 2)

        topo_layer = map_layers.get(layer__slug='topografische-kaart-grijs')
        self.assertEqual(topo_layer.settings, {"customSettings": False})

        afval_layer = map_layers.get(layer__slug='id_beheer_afvalbakken')
        self.assertEqual(afval_layer.settings, {
            "id": 52,
            "slug": "id_beheer_afvalbakken",
            "title": "Beheer Afvalbakken",
            "customSettings": True
        })

    def test_import_empty_layers(self):
        """Test import with empty layers value"""
        row = {'slug': self.map.slug, 'layers': ''}

        self.resource.after_save_instance(self.map, row)

        map_layers = MapLayer.objects.filter(map=self.map)
        self.assertEqual(map_layers.count(), 0)

    def test_import_update_existing_maplayer(self):
        """Test that import updates existing MapLayer records"""
        MapLayer.objects.create(
            map=self.map,
            layer=self.layer1,
            settings={"oldSetting": True}
        )

        layer_data = 'topografische-kaart-grijs::{"newSetting": false}::0::no-category'
        row = {'slug': self.map.slug, 'layers': layer_data}

        self.resource.after_save_instance(self.map, row)

        map_layers = MapLayer.objects.filter(map=self.map)
        self.assertEqual(map_layers.count(), 1)

        layer = map_layers.get(layer__slug='topografische-kaart-grijs')
        self.assertEqual(layer.settings, {"newSetting": False})

    def test_export_categories(self):
        """Test the export (dehydrate) method processes category data correctly"""
        MapCategory.objects.create(
            map=self.map,
            category=self.category1,
            ordering=1
        )
        MapCategory.objects.create(
            map=self.map,
            category=self.category2,
            ordering=2
        )

        result = self.resource.dehydrate_categories(self.map)

        self.assertIn('beheer::1', result)
        self.assertIn('groen::2', result)

        categories_data = result.split("|")
        self.assertEqual(len(categories_data), 2)

    def test_export_empty_categories(self):
        """Test export with no categories"""
        result = self.resource.dehydrate_categories(self.map)
        self.assertEqual(result, '')

    def test_import_categories(self):
        """Test the import (after_save_instance) method creates MapCategory instances"""
        row = {'slug': self.map.slug, 'categories': self.category_data}

        self.resource.after_save_instance(self.map, row)

        map_categories = MapCategory.objects.filter(map=self.map)
        self.assertEqual(map_categories.count(), 2)

        beheer_cat = map_categories.get(category__slug='beheer')
        self.assertEqual(beheer_cat.ordering, 1)

        groen_cat = map_categories.get(category__slug='groen')
        self.assertEqual(groen_cat.ordering, 2)

    def test_import_empty_categories(self):
        """Test import with empty categories value"""
        row = {'slug': self.map.slug, 'categories': ''}

        self.resource.after_save_instance(self.map, row)

        map_categories = MapCategory.objects.filter(map=self.map)
        self.assertEqual(map_categories.count(), 0)

    def test_import_update_existing_mapcategory(self):
        """Test that import updates existing MapCategory records"""
        MapCategory.objects.create(
            map=self.map,
            category=self.category1,
            ordering=5
        )

        category_data = 'beheer::10'
        row = {'slug': self.map.slug, 'categories': category_data}

        self.resource.after_save_instance(self.map, row)

        map_categories = MapCategory.objects.filter(map=self.map)
        self.assertEqual(map_categories.count(), 1)

        category = map_categories.get(category__slug='beheer')
        self.assertEqual(category.ordering, 10)

    def test_import_both_categories_and_layers(self):
        """Test importing both categories and layers together in a single import"""
        row = {
            'slug': self.map.slug,
            'categories': self.category_data,
            'layers': self.layer_data
        }

        self.resource.after_save_instance(self.map, row)

        map_categories = MapCategory.objects.filter(map=self.map)
        self.assertEqual(map_categories.count(), 2)

        map_layers = MapLayer.objects.filter(map=self.map)
        self.assertEqual(map_layers.count(), 2)

    def test_import_layers_with_category_references(self):
        """Test importing layers that reference map categories"""
        row = {'slug': self.map.slug, 'categories': self.category_data}
        self.resource.after_save_instance(self.map, row)

        layer_data_with_categories = (
            'topografische-kaart-grijs::{"opacity": 0.8}::0::beheer|'
            'id_beheer_afvalbakken::{"visible": true}::1::groen'
        )
        row = {'slug': self.map.slug, 'layers': layer_data_with_categories}
        self.resource.after_save_instance(self.map, row)

        topo_layer = MapLayer.objects.get(map=self.map, layer=self.layer1)
        self.assertIsNotNone(topo_layer.map_category)
        self.assertEqual(topo_layer.map_category.category.slug, 'beheer')

        afval_layer = MapLayer.objects.get(map=self.map, layer=self.layer2)
        self.assertIsNotNone(afval_layer.map_category)
        self.assertEqual(afval_layer.map_category.category.slug, 'groen')

    def test_import_layers_with_missing_category_reference(self):
        """Test importing layers that reference non-existent categories"""
        layer_data_with_invalid_category = (
            'topografische-kaart-grijs::{"opacity": 0.8}::0::nonexistent-category'
        )
        row = {'slug': self.map.slug, 'layers': layer_data_with_invalid_category}

        self.resource.after_save_instance(self.map, row)

        topo_layer = MapLayer.objects.get(map=self.map, layer=self.layer1)
        self.assertIsNone(topo_layer.map_category)

    def test_full_import_export_roundtrip(self):
        """Test that exported data can be re-imported correctly"""
        MapCategory.objects.create(
            map=self.map,
            category=self.category1,
            ordering=1
        )
        MapCategory.objects.create(
            map=self.map,
            category=self.category2,
            ordering=2
        )

        MapLayer.objects.create(
            map=self.map,
            layer=self.layer1,
            settings={"opacity": 0.8},
            ordering=0
        )
        MapLayer.objects.create(
            map=self.map,
            layer=self.layer2,
            settings={"visible": True},
            ordering=1
        )

        exported_categories = self.resource.dehydrate_categories(self.map)
        exported_layers = self.resource.dehydrate_layers(self.map)

        new_map = Map.objects.create(
            title='new-map',
            slug='new-map',
            published=False,
            show_in_overview=True
        )

        row = {
            'slug': new_map.slug,
            'categories': exported_categories,
            'layers': exported_layers
        }

        self.resource.after_save_instance(new_map, row)

        new_map_categories = MapCategory.objects.filter(map=new_map)
        self.assertEqual(new_map_categories.count(), 2)

        new_map_layers = MapLayer.objects.filter(map=new_map)
        self.assertEqual(new_map_layers.count(), 2)

    def test_import_updates_existing_both_categories_and_layers(self):
        """Test that importing updates existing categories and layers"""
        MapCategory.objects.create(
            map=self.map,
            category=self.category1,
            ordering=1
        )
        MapCategory.objects.create(
            map=self.map,
            category=self.category2,
            ordering=2
        )

        MapLayer.objects.create(
            map=self.map,
            layer=self.layer1,
            settings={"old": True},
            ordering=5
        )

        new_category_data = 'beheer::10|groen::20'
        new_layer_data = 'topografische-kaart-grijs::{"new": true}::100::no-category'

        row = {
            'slug': self.map.slug,
            'categories': new_category_data,
            'layers': new_layer_data
        }

        self.resource.after_save_instance(self.map, row)

        beheer_cat = MapCategory.objects.get(map=self.map, category=self.category1)
        self.assertEqual(beheer_cat.ordering, 10)

        groen_cat = MapCategory.objects.get(map=self.map, category=self.category2)
        self.assertEqual(groen_cat.ordering, 20)

        topo_layer = MapLayer.objects.get(map=self.map, layer=self.layer1)
        self.assertEqual(topo_layer.settings, {"new": True})
        self.assertEqual(topo_layer.ordering, 100)

