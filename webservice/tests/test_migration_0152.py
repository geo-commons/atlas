import importlib

from django.apps import apps
from django.test import TransactionTestCase

module = importlib.import_module('webservice.migrations.0152_map_position_settings')
backfill_map_positions = module.backfill_map_positions


class Migration0152Test(TransactionTestCase):
    def setUp(self):
        self.Map = apps.get_model('webservice', 'Map')

    def test_backfill_map_positions_uses_current_constance_values(self):
        original_zoom = module.config.POSITION_ZOOM
        original_center_x = module.config.POSITION_CENTER_X
        original_center_y = module.config.POSITION_CENTER_Y

        try:
            module.config.POSITION_ZOOM = 8.5
            module.config.POSITION_CENTER_X = 100.1
            module.config.POSITION_CENTER_Y = 200.2

            map_instance = self.Map.objects.create(title='Test Map', slug='test-map', settings={})

            backfill_map_positions(apps, None)

            map_instance.refresh_from_db()
            self.assertEqual(
                map_instance.settings['position'],
                {
                    'zoom': 8.5,
                    'center': {
                        'x': 100.1,
                        'y': 200.2,
                    },
                },
            )
        finally:
            module.config.POSITION_ZOOM = original_zoom
            module.config.POSITION_CENTER_X = original_center_x
            module.config.POSITION_CENTER_Y = original_center_y

    def test_backfill_map_positions_keeps_existing_map_position(self):
        map_instance = self.Map.objects.create(
            title='Test Map',
            slug='test-map',
            settings={
                'position': {
                    'zoom': 4,
                    'center': {
                        'x': 1,
                        'y': 2,
                    },
                },
            },
        )

        backfill_map_positions(apps, None)

        map_instance.refresh_from_db()
        self.assertEqual(
            map_instance.settings['position'],
            {
                'zoom': 4,
                'center': {
                    'x': 1,
                    'y': 2,
                },
            },
        )
