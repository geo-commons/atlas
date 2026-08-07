from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from webservice.models import Source
from webservice.viewsets import SourceViewSet


class DuplicateActionTest(APITestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)

    def test_duplicate_rejects_empty_ids(self):
        response = self.client.post(
            '/atlas/api/v1/sources/duplicate/',
            {'ids': []},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'No objects were selected for duplication.')

    def test_duplicate_rejects_missing_ids(self):
        source = Source.objects.create(
            title='Existing source',
            slug='existing-source',
            url='https://example.com/api',
        )
        missing_id = source.id + 1

        response = self.client.post(
            '/atlas/api/v1/sources/duplicate/',
            {'ids': [source.id, missing_id]},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Some objects could not be duplicated.')
        self.assertEqual(response.data['ids'], [str(missing_id)])
        self.assertEqual(Source.objects.filter(title='Existing source (2)').count(), 0)

    def test_duplicate_rolls_back_when_one_object_fails(self):
        first_source = Source.objects.create(
            title='First source',
            slug='first-source',
            url='https://example.com/first',
        )
        second_source = Source.objects.create(
            title='Second source',
            slug='second-source',
            url='https://example.com/second',
        )

        with patch.object(SourceViewSet, 'after_duplicate', side_effect=[None, RuntimeError('duplicate failed')]):
            with self.assertRaises(RuntimeError):
                self.client.post(
                    '/atlas/api/v1/sources/duplicate/',
                    {'ids': [first_source.id, second_source.id]},
                    format='json',
                )

        self.assertFalse(Source.objects.filter(title='First source (2)').exists())
        self.assertFalse(Source.objects.filter(title='Second source (2)').exists())
