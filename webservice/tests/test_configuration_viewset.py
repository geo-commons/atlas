from constance import config
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class ConfigurationViewSetTest(APITestCase):
    url = '/atlas/api/v1/configurations/'

    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)
        self.original_site_id = config.MATOMO_SITE_ID
        config.MATOMO_SITE_ID = '1'

    def tearDown(self):
        config.MATOMO_SITE_ID = self.original_site_id

    def test_rejects_invalid_matomo_site_ids(self):
        invalid_site_ids = (
            '1]); alert(1); //',
            '1.5',
            '-1',
            '1e2',
            '<script>alert(1)</script>',
        )

        for site_id in invalid_site_ids:
            with self.subTest(site_id=site_id):
                response = self.client.post(self.url, {'MATOMO_SITE_ID': site_id}, format='multipart')

                self.assertEqual(response.status_code, 400)
                self.assertEqual(config.MATOMO_SITE_ID, '1')

    def test_accepts_numeric_matomo_site_id_as_string(self):
        response = self.client.post(self.url, {'MATOMO_SITE_ID': '123'}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(config.MATOMO_SITE_ID, '123')

    def test_accepts_empty_matomo_site_id(self):
        response = self.client.post(self.url, {'MATOMO_SITE_ID': ''}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(config.MATOMO_SITE_ID, '')
