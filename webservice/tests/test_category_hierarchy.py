from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from rest_framework.test import APITestCase

from webservice.models import Category, Layer, Source
from webservice.serializers import (
    CategorySerializer,
    LayerCreateUpdateSerializer,
    LayerSerializer,
)


class CategoryHierarchyTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parent_category = Category.objects.create(
            title='Infrastructure',
            slug='infrastructure',
        )
        self.subcategory = Category.objects.create(
            title='Roads',
            slug='roads',
            parent=self.parent_category,
        )
        self.source = Source.objects.create(
            title='Source',
            slug='source',
            url='https://example.com',
        )

    def test_category_serializer_includes_parent_and_full_title(self):
        serializer = CategorySerializer(self.subcategory)

        self.assertEqual(serializer.data['parent_id'], self.parent_category.id)
        self.assertEqual(serializer.data['full_title'], 'Infrastructure / Roads')
        self.assertEqual(serializer.data['parent']['id'], self.parent_category.id)
        self.assertEqual(serializer.data['parent']['title'], self.parent_category.title)
        
    def test_category_serializer_allows_creating_category_without_parent(self):
        serializer = CategorySerializer(
            data={
                'title': 'New Category',
                'slug': 'new-category',
            }
        )

        self.assertTrue(serializer.is_valid())
        category = serializer.save()

        self.assertIsNone(category.parent)
        self.assertEqual(category.title, 'New Category')
        self.assertEqual(category.slug, 'new-category')

    def test_category_serializer_rejects_self_as_parent(self):
        serializer = CategorySerializer(
            instance=self.parent_category,
            data={'parent_id': self.parent_category.id},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['parent_id'][0],
            'Het is niet mogelijk om een categorie zichzelf als hoofdcategorie te selecteren.',
        )

    def test_category_serializer_rejects_subcategory_as_parent(self):
        serializer = CategorySerializer(
            data={
                'title': 'Lane closures',
                'slug': 'lane-closures',
                'parent_id': self.subcategory.id,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['parent_id'][0],
            'Het is niet mogelijk om een subcategorie als hoofdcategorie te selecteren.',
        )

    def test_category_serializer_rejects_parent_for_category_with_children(self):
        other_parent_category = Category.objects.create(
            title='Public space',
            slug='public-space',
        )
        serializer = CategorySerializer(
            instance=self.parent_category,
            data={'parent_id': other_parent_category.id},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['parent_id'][0],
            'Het is niet mogelijk om een hoofdcategorie met subcategorieën als subcategorie te selecteren.',
        )

    def test_layer_create_update_serializer_accepts_subcategory(self):
        layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
        )
        serializer = LayerCreateUpdateSerializer(
            instance=layer,
            data={'category_id': self.subcategory.id},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_layer = serializer.save()

        self.assertEqual(updated_layer.layer_type, self.subcategory)

    def test_layer_serializer_includes_parent_for_subcategory(self):
        layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=self.subcategory,
            published=True,
        )
        request = self.factory.get('/')
        request.user = AnonymousUser()

        serializer = LayerSerializer(layer, context={'request': request})

        self.assertEqual(serializer.data['category']['id'], self.subcategory.id)
        self.assertEqual(serializer.data['category']['full_title'], 'Infrastructure / Roads')
        self.assertEqual(serializer.data['category']['parent']['id'], self.parent_category.id)

    def test_layer_to_dict_includes_parent_for_subcategory(self):
        layer = Layer.objects.create(
            title='Traffic incidents',
            slug='traffic-incidents',
            layer_name='atlas:traffic_incidents',
            layer_source=self.source,
            layer_type=self.subcategory,
        )
        request = self.factory.get('/')
        request.user = AnonymousUser()

        serialized_layer = layer.to_dict(request.user, request)

        self.assertEqual(serialized_layer['category']['id'], self.subcategory.id)
        self.assertEqual(serialized_layer['category']['full_title'], 'Infrastructure / Roads')
        self.assertEqual(serialized_layer['category']['parent']['id'], self.parent_category.id)


class CategoryDeleteViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)
        self.parent_category = Category.objects.create(
            title='Infrastructure',
            slug='infrastructure',
        )
        self.subcategory = Category.objects.create(
            title='Roads',
            slug='roads',
            parent=self.parent_category,
        )

    def test_delete_detail_rejects_parent_category_with_subcategories(self):
        response = self.client.delete(f'/atlas/api/v1/categories/{self.parent_category.id}/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['detail'],
            'Het is niet mogelijk om een hoofdcategorie met subcategorieën te verwijderen.',
        )
        self.assertTrue(Category.objects.filter(id=self.parent_category.id).exists())
        self.assertTrue(Category.objects.filter(id=self.subcategory.id).exists())

    def test_delete_bulk_rejects_parent_category_with_subcategories(self):
        response = self.client.post(
            '/atlas/api/v1/categories/delete/',
            {'ids': [self.parent_category.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['detail'],
            'Het is niet mogelijk om een hoofdcategorie met subcategorieën te verwijderen.',
        )
        self.assertTrue(Category.objects.filter(id=self.parent_category.id).exists())
        self.assertTrue(Category.objects.filter(id=self.subcategory.id).exists())
