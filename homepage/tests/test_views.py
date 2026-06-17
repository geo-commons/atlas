from inertia.test import InertiaTestCase

from webservice.models import Category, Layer, Map, MapCategory, MapLayer, Source


class HomepageViewsTest(InertiaTestCase):
    def setUp(self):
        super().setUp()
        self.source = Source.objects.create(
            title='Source',
            slug='source',
            url='https://example.com',
        )
        self.main_map, _ = Map.objects.update_or_create(
            is_main=True,
            defaults={
                'title': 'Main Map',
                'slug': 'main-map',
                'published': True,
                'show_in_overview': False,
                'settings': {
                    'position': {
                        'zoom': 7,
                        'center': {
                            'x': 11,
                            'y': 22,
                        },
                    },
                },
            },
        )

    def test_atlas_root_renders_configured_main_map(self):

        response = self.client.get('/atlas/')

        self.assertEqual(response.status_code, 200)
        self.assertComponentUsed('Map')
        self.assertIncludesTemplateData({'title': 'Atlas', 'vite_entry': 'src/map.js'})
        self.assertContains(response, 'data-page="app"')
        self.assertEqual(self.props()['map']['slug'], self.main_map.slug)
        self.assertTrue(self.props()['map']['is_main'])
        self.assertEqual(self.props()['config']['position'], self.main_map.settings['position'])

    def test_v3_includes_flat_map_layers_and_categories_with_subcategories(self):
        parent_category = Category.objects.create(title='Infrastructure', slug='infrastructure', ordering=30)
        subcategory = Category.objects.create(title='Roads', slug='roads', ordering=20, parent=parent_category)
        direct_layer = Layer.objects.create(
            title='Public lights',
            slug='public-lights',
            layer_name='atlas:public_lights',
            layer_source=self.source,
            layer_type=parent_category,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        subcategory_layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=subcategory,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        parent_map_category = MapCategory.objects.create(map=self.main_map, category=parent_category, ordering=3)
        subcategory_map_category = MapCategory.objects.create(map=self.main_map, category=subcategory, ordering=1)
        MapLayer.objects.create(
            map=self.main_map,
            layer=direct_layer,
            map_category=parent_map_category,
            ordering=2,
            settings={},
        )
        MapLayer.objects.create(
            map=self.main_map,
            layer=subcategory_layer,
            map_category=subcategory_map_category,
            ordering=1,
            settings={},
        )

        self.client.get('/atlas/')

        layer_ids = [layer['id'] for layer in self.props()['layers']]
        self.assertIn('public-lights', layer_ids)
        self.assertIn('traffic-incidents', layer_ids)

        map_data = self.props()['map']
        self.assertEqual(
            map_data['categories'],
            [
                {'category': subcategory.id, 'ordering': subcategory_map_category.ordering},
                {'category': parent_category.id, 'ordering': parent_map_category.ordering},
            ],
        )
        self.assertEqual([layer['layer'] for layer in map_data['layers']], [subcategory_layer.id, direct_layer.id])

    def test_v3_includes_map_categories_for_frontend_tree_building(self):
        parent_category = Category.objects.create(title='Infrastructure', slug='infrastructure', ordering=30)
        subcategory = Category.objects.create(title='Roads', slug='roads', ordering=20, parent=parent_category)
        subcategory_layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=subcategory,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        subcategory_map_category = MapCategory.objects.create(map=self.main_map, category=subcategory, ordering=1)
        MapLayer.objects.create(
            map=self.main_map,
            layer=subcategory_layer,
            map_category=subcategory_map_category,
            ordering=1,
            settings={},
        )

        self.client.get('/atlas/')

        layer_ids = [layer['id'] for layer in self.props()['layers']]
        self.assertIn('traffic-incidents', layer_ids)

        map_data = self.props()['map']
        self.assertEqual(map_data['categories'], [{'category': subcategory.id, 'ordering': 1}])

    def test_v3_map_layers_include_configured_layers_only(self):        
        category = Category.objects.create(title='Infrastructure', slug='infrastructure')
        configured_layer = Layer.objects.create(
            title='Public lights',
            slug='public-lights',
            layer_name='atlas:public_lights',
            layer_source=self.source,
            layer_type=category,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        unconfigured_layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=category,
            published=True,
            closed_dataset=False,
            login_required=False,
        )
        unpublished_layer = Layer.objects.create(
            title='Road works',
            slug='road-works',
            layer_name='atlas:road_works',
            layer_source=self.source,
            layer_type=category,
            published=False,
            closed_dataset=False,
            login_required=False,
        )
        map_category = MapCategory.objects.create(map=self.main_map, category=category, ordering=1)
        MapLayer.objects.create(
            map=self.main_map,
            layer=configured_layer,
            map_category=map_category,
            ordering=1,
            settings={},
        )
        MapLayer.objects.create(
            map=self.main_map,
            layer=unpublished_layer,
            map_category=map_category,
            ordering=2,
            settings={},
        )

        self.client.get('/atlas/')

        layer_ids = [layer['id'] for layer in self.props()['layers']]
        self.assertIn('public-lights', layer_ids)
        self.assertIn('traffic-incidents', layer_ids)
        self.assertNotIn('road-works', layer_ids)

        map_layer_ids = [layer['layer'] for layer in self.props()['map']['layers']]
        self.assertEqual(map_layer_ids, [configured_layer.id, unpublished_layer.id])
        self.assertNotIn(unconfigured_layer.id, map_layer_ids)
