from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from webservice.models import Map


class MapViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)

    def test_delete_detail_rejects_main_map(self):
        main_map, _ = Map.objects.update_or_create(
            is_main=True,
            defaults={
                'title': 'Current Main',
                'slug': 'current-main',
                'published': True,
                'show_in_overview': False,
            },
        )

        response = self.client.delete(f'/atlas/api/v1/maps/{main_map.id}/')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(Map.objects.filter(id=main_map.id).exists())

    def test_delete_bulk_rejects_main_map(self):
        main_map, _ = Map.objects.update_or_create(
            is_main=True,
            defaults={
                'title': 'Current Main',
                'slug': 'current-main',
                'published': True,
                'show_in_overview': False,
            },
        )
        other_map = Map.objects.create(title='Other', slug='other-map')

        response = self.client.post(
            '/atlas/api/v1/maps/delete/',
            {'ids': [main_map.id, other_map.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(Map.objects.filter(id=main_map.id).exists())
        self.assertTrue(Map.objects.filter(id=other_map.id).exists())
