from random import choice

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from user_management.models import AtlasUser


class TestAdminFromTheBigBadInternet(TestCase):
    def setUp(self):
        self.client = Client(REMOTE_ADDR='1.2.3.4')

    def test_persmission_admin_login(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 403)

    def test_persmission_admin_listing(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 403)


class TestAdminFromCtrix(TestCase):
    def setUp(self):
        self.client = Client(REMOTE_ADDR=choice(settings.CTRIX_IPS))

    def test_persmission_admin_login(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)

    def test_persmission_admin_listing_redirect(self):
        """Expect 302 (redirect), because user is not logged in."""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_persmission_admin_listing_logged_in(self):
        """Expect 200 , because user is staff user."""
        cred = {'username': 'testuser', 'password': '1234'}
        user = AtlasUser(**cred)
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
