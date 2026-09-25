from constance import config
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class ConfigurationViewSetTest(APITestCase):
    url = '/atlas/api/v1/configurations/'
    color_settings = (
        'ORGANIZATION_PRIMARY_COLOR',
        'ORGANIZATION_TITLE_COLOR',
        'ORGANIZATION_TEXT_COLOR',
    )

    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)
        self.original_colors = {key: getattr(config, key) for key in self.color_settings}

        for key in self.color_settings:
            setattr(config, key, '#000000')

    def tearDown(self):
        for key, value in self.original_colors.items():
            setattr(config, key, value)

    def test_rejects_invalid_organization_colors(self):
        invalid_colors = ('!NOT_A_VALID_COLOR!', 'red', '#123', '#12345G', '#123456; display: none')

        for key in self.color_settings:
            for invalid_color in invalid_colors:
                with self.subTest(key=key, value=invalid_color):
                    response = self.client.post(self.url, {key: invalid_color}, format='multipart')

                    self.assertEqual(response.status_code, 400)
                    self.assertEqual(getattr(config, key), '#000000')

    def test_accepts_valid_organization_colors(self):
        colors = {
            'ORGANIZATION_PRIMARY_COLOR': '#12aBcD',
            'ORGANIZATION_TITLE_COLOR': '#A1B2C3',
            'ORGANIZATION_TEXT_COLOR': '#abcdef',
        }

        response = self.client.post(self.url, colors, format='multipart')

        self.assertEqual(response.status_code, 200)
        for key, value in colors.items():
            self.assertEqual(getattr(config, key), value)

    def test_accepts_empty_organization_colors(self):
        response = self.client.post(
            self.url,
            {
                'ORGANIZATION_PRIMARY_COLOR': '',
                'ORGANIZATION_TITLE_COLOR': '',
                'ORGANIZATION_TEXT_COLOR': '',
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(config.ORGANIZATION_PRIMARY_COLOR, '')
        self.assertEqual(config.ORGANIZATION_TITLE_COLOR, '')
        self.assertEqual(config.ORGANIZATION_TEXT_COLOR, '')

    def test_rejects_entire_request_when_one_color_is_invalid(self):
        response = self.client.post(
            self.url,
            {
                'ORGANIZATION_PRIMARY_COLOR': '#123456',
                'ORGANIZATION_TITLE_COLOR': 'invalid',
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(config.ORGANIZATION_PRIMARY_COLOR, '#000000')
