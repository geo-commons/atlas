import json

from django.test import TestCase

from webservice.models import Layer, MapLayer, Map
from webservice.widgets import MapLayerManyToManyWidget

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

        self.map = Map.objects.create(
            title='afvalbakken',
            slug='afvalbakken',
            published=False,
            show_in_overview=True
        )

        self.layer_data = "topografische-kaart-grijs:{\"customSettings\": false}|id_beheer_afvalbakken:{\"id\": 52, \"slug\": \"id_beheer_afvalbakken\", \"title\": \"Beheer Afvalbakken\", \"customSettings\": true}"

        self.widget = MapLayerManyToManyWidget(
            model=Layer,
            through_model=MapLayer,
            map_field='map',
            layer_field='layer',
            field='slug',
            separator='|'
        )

    def test_clean_method(self):
        """Test the clean (import) method processes layer data correctly and creates MapLayer instances"""
        row = {'slug': self.map.slug}

        layers = self.widget.clean(self.layer_data, row)

        self.assertEqual(len(layers), 2)

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

    def test_clean_method_with_empty_value(self):
        """Test clean (import) method with empty input"""
        result = self.widget.clean("", {'slug': self.map.slug})
        self.assertEqual(result, [])

    def test_clean_method_with_map_that_not_exists(self):
        """Test clean (import) method with map that not exists"""
        result = self.widget.clean(self.layer_data, {'slug': "not-existing-map"})
        self.assertEqual(result, [])

    def test_clean_method_without_row_slug(self):
        """Test clean (import) method without row slug"""
        result = self.widget.clean(self.layer_data, {'kort-kenmerk': 'not-existing-slug'})
        self.assertEqual(result, [])

    def test_render_method(self):
        """Test full render (export) method"""
        self.widget.clean(self.layer_data, {'slug': self.map.slug})

        result = self.widget.render(True, self.map)

        layers_data = result.split("|")
        self.assertEqual(len(layers_data), 2)

        for layer_string in layers_data:
            slug, settings_json = layer_string.split(':', 1)
            settings = json.loads(settings_json)

            if slug == 'topografische-kaart-grijs':
                self.assertEqual(settings, {"customSettings": False})
            elif slug == 'id_beheer_afvalbakken':
                self.assertTrue('customSettings' in settings)

    def test_render_method_with_empty_value(self):
        """Test render (export) method with empty input"""
        result = self.widget.render("", self.map);
        self.assertEqual(result, '')