from django.test import SimpleTestCase
from django.urls import resolve

from homepage import views


class MapUrlTests(SimpleTestCase):
    def test_maps_root_resolves_without_slug(self):
        match = resolve('/atlas/maps/')

        self.assertEqual(match.view_name, 'homepage:v3_map')
        self.assertEqual(match.func, views.v3)
        self.assertEqual(match.kwargs, {})

    def test_plain_map_urls_resolve_with_full_slug(self):
        cases = (
            ('/atlas/maps/luchtfotos', 'luchtfotos'),
            ('/atlas/maps/LuchtFotos-2021', 'LuchtFotos-2021'),
            ('/atlas/maps/wegen-2024/', 'wegen-2024'),
        )

        for url, slug in cases:
            with self.subTest(url=url):
                self.assert_map_url_slug(url, slug)

    def test_map_urls_with_frontend_configuration_pass_only_slug_to_view(self):
        cases = (
            ('/atlas/maps/luchtfotos@126910.00,505834.00,13z/layers=/base=luchtfoto-2021', 'luchtfotos'),
            (
                '/atlas/maps/LuchtFotos-2021/@126910.00,505834.00,13z/layers=wegen,water/base=luchtfoto-2021',
                'LuchtFotos-2021',
            ),
        )

        for url, slug in cases:
            with self.subTest(url=url):
                self.assert_map_url_slug(url, slug)

    def assert_map_url_slug(self, url: str, slug: str) -> None:
        match = resolve(url)

        self.assertEqual(match.view_name, 'homepage:v3_map')
        self.assertEqual(match.func, views.v3)
        self.assertEqual(match.kwargs, {'slug': slug})
