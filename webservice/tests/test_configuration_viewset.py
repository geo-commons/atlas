import shutil
import tempfile
from io import BytesIO

from constance import config
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.test import override_settings
from PIL import Image
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
        invalid_colors = ('!NOT_A_VALID_COLOR!', 'red', '#123', '#1234567', '#12345G', '#123456; display: none')

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


class ConfigurationImageUploadViewSetTest(APITestCase):
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

    @override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=0)
    def test_rejects_invalid_temporary_image_upload(self):
        uploaded_file = SimpleUploadedFile(
            'logo.svg',
            b'This is not an image.',
            content_type='image/svg+xml',
        )

        response = self.client.post(
            '/atlas/api/v1/configurations/',
            {'ORGANIZATION_LOGO': uploaded_file},
            format='multipart',
        )

        self.assertIsInstance(response.wsgi_request.FILES['ORGANIZATION_LOGO'], TemporaryUploadedFile)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(config.ORGANIZATION_LOGO, '')
        self.assertFalse(default_storage.exists('logo.svg'))

    @override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=0)
    def test_accepts_valid_temporary_image_uploads(self):
        images = (
            ('logo.svg', b'<svg xmlns="http://www.w3.org/2000/svg"></svg>', 'image/svg+xml'),
            ('logo.png', self._create_png(), 'image/png'),
        )

        for filename, content, content_type in images:
            with self.subTest(filename=filename):
                uploaded_file = SimpleUploadedFile(filename, content, content_type=content_type)

                response = self.client.post(
                    '/atlas/api/v1/configurations/',
                    {'ORGANIZATION_LOGO': uploaded_file},
                    format='multipart',
                )

                self.assertIsInstance(response.wsgi_request.FILES['ORGANIZATION_LOGO'], TemporaryUploadedFile)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(config.ORGANIZATION_LOGO, filename)
                with default_storage.open(filename, 'rb') as stored_file:
                    self.assertEqual(stored_file.read(), content)
