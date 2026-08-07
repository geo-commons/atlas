from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from authz.models import Authorization
from user_management.models import AtlasGroup
from webservice.models import Source


class AuthorizationViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)

    def test_duplicate_copies_authorization_with_groups(self):
        read_group = AtlasGroup.objects.create(name='Read group')
        write_group = AtlasGroup.objects.create(name='Write group')
        source = Source.objects.create(
            title='Source',
            slug='source',
            url='https://example.com/ows',
        )
        authorization = Authorization.objects.create(
            source=source,
            ordering=7,
            resource='atlas:protected_layer',
            description='Protected layer authorization',
            login_required=False,
            only_internal=False,
            authenticated_can_mutate=True,
            audit_log=False,
            response_filter='.features[]',
        )
        authorization.atlas_groups.set([read_group])
        authorization.atlas_write_groups.set([write_group])

        response = self.client.post(
            '/atlas/api/v1/authorizations/duplicate/',
            {'ids': [authorization.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Authorization.objects.filter(resource='atlas:protected_layer').count(), 2)

        duplicated_authorization = Authorization.objects.exclude(id=authorization.id).get(resource='atlas:protected_layer')
        self.assertEqual(duplicated_authorization.source, source)
        self.assertEqual(duplicated_authorization.ordering, 7)
        self.assertEqual(duplicated_authorization.description, 'Protected layer authorization')
        self.assertFalse(duplicated_authorization.login_required)
        self.assertFalse(duplicated_authorization.only_internal)
        self.assertTrue(duplicated_authorization.authenticated_can_mutate)
        self.assertFalse(duplicated_authorization.audit_log)
        self.assertEqual(duplicated_authorization.response_filter, '.features[]')
        self.assertEqual(list(duplicated_authorization.atlas_groups.all()), [read_group])
        self.assertEqual(list(duplicated_authorization.atlas_write_groups.all()), [write_group])
