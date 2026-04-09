from django.test import TestCase

from webservice.models import Map


class HomepageViewsTest(TestCase):
    def test_atlas_root_renders_configured_main_map(self):
        main_map, _ = Map.objects.update_or_create(
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

        response = self.client.get('/atlas/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'v3/map.html')
        self.assertEqual(response.context['data']['map']['slug'], main_map.slug)
        self.assertTrue(response.context['data']['map']['is_main'])
        self.assertEqual(response.context['data']['config']['position'], main_map.settings['position'])
