from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from webservice.models import Viewer


class ViewerViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)

    def test_duplicate_copies_viewer(self):
        viewer = Viewer.objects.create(
            ordering=3,
            label='Street viewer',
            type=Viewer.TYPE_IFRAME,
            username='viewer-user',
            password='viewer-password',
            api_key='viewer-api-key',
            url='https://example.com/viewer',
            is_oblique=True,
            internal=False,
        )

        response = self.client.post(
            '/atlas/api/v1/viewers/duplicate/',
            {'ids': [viewer.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)

        duplicated_viewer = Viewer.objects.get(label='Street viewer (2)')
        self.assertEqual(duplicated_viewer.ordering, 3)
        self.assertEqual(duplicated_viewer.type, Viewer.TYPE_IFRAME)
        self.assertEqual(duplicated_viewer.username, 'viewer-user')
        self.assertEqual(duplicated_viewer.password, 'viewer-password')
        self.assertEqual(duplicated_viewer.api_key, 'viewer-api-key')
        self.assertEqual(duplicated_viewer.url, 'https://example.com/viewer')
        self.assertTrue(duplicated_viewer.is_oblique)
        self.assertFalse(duplicated_viewer.internal)
