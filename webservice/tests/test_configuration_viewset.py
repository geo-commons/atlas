import shutil
import tempfile
from io import BytesIO

from constance import config
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase


class ConfigurationViewSetTest(APITestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.override_settings = override_settings(MEDIA_ROOT=self.media_root)
        self.override_settings.enable()

        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)
        config.ORGANIZATION_LOGO = ''
        config.ORGANIZATION_NAME = 'Gemeente Purmerend'

    def tearDown(self):
        self.override_settings.disable()
        shutil.rmtree(self.media_root)

    def test_rejects_non_image_file_for_organization_logo(self):
        uploaded_file = SimpleUploadedFile(
            'logo.png',
            b'This is not an image.',
            content_type='image/png',
        )

        response = self.client.post(
            '/atlas/api/v1/configurations/',
            {'ORGANIZATION_LOGO': uploaded_file},
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(config.ORGANIZATION_LOGO, '')

    def test_rejects_file_upload_for_non_image_configuration(self):
        uploaded_file = SimpleUploadedFile(
            'organization.txt',
            b'Gemeente Purmerend',
            content_type='text/plain',
        )

        response = self.client.post(
            '/atlas/api/v1/configurations/',
            {'ORGANIZATION_NAME': uploaded_file},
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(config.ORGANIZATION_NAME, 'Gemeente Purmerend')

    def test_accepts_valid_image_for_organization_logo(self):
        uploaded_file = SimpleUploadedFile(
            'logo.png',
            self._create_png(),
            content_type='image/png',
        )

        response = self.client.post(
            '/atlas/api/v1/configurations/',
            {'ORGANIZATION_LOGO': uploaded_file},
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(config.ORGANIZATION_LOGO, 'logo.png')

    def _create_png(self):
        image_file = BytesIO()
        Image.new('RGB', (1, 1), color='white').save(image_file, format='PNG')
        return image_file.getvalue()
