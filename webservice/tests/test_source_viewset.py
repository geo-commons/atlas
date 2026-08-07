from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from user_management.models import AtlasGroup
from webservice.models import Source


class SourceViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)

    def test_duplicate_copies_source_with_groups(self):
        group = AtlasGroup.objects.create(name='Source group')
        source = Source.objects.create(
            title='Protected source',
            slug='protected-source',
            source_type=Source.SOURCE_REST,
            url='https://example.com/api',
            login_required=True,
            authenticate=True,
        )
        source.atlas_groups.set([group])

        response = self.client.post(
            '/atlas/api/v1/sources/duplicate/',
            {'ids': [source.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)

        duplicated_source = Source.objects.get(title='Protected source (2)')
        self.assertEqual(duplicated_source.slug, 'protected-source-2')
        self.assertEqual(duplicated_source.source_type, Source.SOURCE_REST)
        self.assertEqual(duplicated_source.url, 'https://example.com/api')
        self.assertTrue(duplicated_source.login_required)
        self.assertTrue(duplicated_source.authenticate)
        self.assertEqual(list(duplicated_source.atlas_groups.all()), [group])
