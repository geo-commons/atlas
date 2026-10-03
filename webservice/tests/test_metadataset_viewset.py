from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from webservice.models import Metadataset


class TestMetadatasetPermissions(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            password='password123',
        )
        self.staff_user = get_user_model().objects.create_user(
            username='staff',
            password='password123',
            is_staff=True,
        )
        self.superuser_without_staff = get_user_model().objects.create_user(
            username='superuser-without-staff',
            password='password123',
            is_superuser=True,
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.metadataset = Metadataset.objects.create(
            title='Published dataset',
            status='completed',
        )
        self.detail_url = f'/atlas/api/v1/metadatasets/{self.metadataset.id}/'

    def test_standard_user_cannot_create_metadataset(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            '/atlas/api/v1/metadatasets/',
            {'title': 'Unauthorized dataset', 'status': 'completed'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Metadataset.objects.filter(title='Unauthorized dataset').exists())

    def test_standard_user_cannot_update_published_metadataset(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.detail_url, {'title': 'Changed title'}, format='json')

        self.assertEqual(response.status_code, 403)
        self.metadataset.refresh_from_db()
        self.assertEqual(self.metadataset.title, 'Published dataset')

    def test_standard_user_cannot_delete_published_metadataset(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Metadataset.objects.filter(pk=self.metadataset.pk).exists())

    def test_user_needs_both_admin_flags_to_update_metadataset(self):
        for user in [self.staff_user, self.superuser_without_staff]:
            with self.subTest(user=user.username):
                self.client.force_authenticate(user)

                response = self.client.patch(self.detail_url, {'title': 'Changed title'}, format='json')

                self.assertEqual(response.status_code, 403)

        self.metadataset.refresh_from_db()
        self.assertEqual(self.metadataset.title, 'Published dataset')

    def test_admin_can_delete_published_metadataset(self):
        self.client.force_authenticate(self.admin_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Metadataset.objects.filter(pk=self.metadataset.pk).exists())
