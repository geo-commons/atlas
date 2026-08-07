from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from user_management.models import AtlasGroup
from webservice.models import Category, Layer, Source


class LayerViewSetTest(APITestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(admin_user)

    def test_duplicate_copies_access_groups(self):
        read_group = AtlasGroup.objects.create(name='Layer read group')
        write_group = AtlasGroup.objects.create(name='Layer write group')
        source = Source.objects.create(
            title='Layer source',
            slug='layer-source',
            url='https://example.com/ows',
        )
        category = Category.objects.create(title='Layer category', slug='layer-category')
        layer = Layer.objects.create(
            title='Protected layer',
            slug='protected-layer',
            layer_name='protected:layer',
            layer_source=source,
            layer_type=category,
        )
        layer.atlas_groups.set([read_group])
        layer.atlas_write_groups.set([write_group])

        response = self.client.post(
            '/atlas/api/v1/layers/duplicate/',
            {'ids': [layer.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        duplicated_layer = Layer.objects.get(title='Protected layer (2)')
        self.assertEqual(list(duplicated_layer.atlas_groups.all()), [read_group])
        self.assertEqual(list(duplicated_layer.atlas_write_groups.all()), [write_group])
