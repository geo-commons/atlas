from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from webservice.models import Category


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.admin_user)

    def test_duplicate_copies_category_parent(self):
        parent_category = Category.objects.create(
            title='Parent category',
            slug='parent-category',
            ordering=1,
        )
        category = Category.objects.create(
            title='Subcategory',
            slug='subcategory',
            ordering=4,
            parent=parent_category,
        )

        response = self.client.post(
            '/atlas/api/v1/categories/duplicate/',
            {'ids': [category.id]},
            format='json',
        )

        self.assertEqual(response.status_code, 201)

        duplicated_category = Category.objects.get(title='Subcategory (2)')
        self.assertEqual(duplicated_category.slug, 'subcategory-2')
        self.assertEqual(duplicated_category.ordering, 4)
        self.assertEqual(duplicated_category.parent, parent_category)
