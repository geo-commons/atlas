from django.test import TestCase, RequestFactory
from user_management.models import AtlasGroup, AtlasUser
from unittest.mock import patch
from .models import Layer


class TestLayerManager(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.group = AtlasGroup.objects.create(name='Test')

        self.user = AtlasUser.objects.create_user(
            username='testuser', password='12345')
        self.user_with_group = AtlasUser.objects.create_user(
            username='another_testuser', password='12345')
        self.user_with_group.atlas_groups.add(self.group)

        self.superuser = AtlasUser.objects.create_superuser(
            username='admin', password='12345')

        self.public_layer = Layer.objects.create(
            closed_dataset=False, login_required=False)
        self.internal_layer = Layer.objects.create(
            closed_dataset=True, login_required=False)
        self.login_required_layer = Layer.objects.create(
            closed_dataset=False, login_required=True)
        self.internal_login_required_layer = Layer.objects.create(
            closed_dataset=True, login_required=True)
        self.layer_only_for_group = Layer.objects.create(
            closed_dataset=False)
        self.layer_only_for_group.atlas_groups.add(self.group)

    def test_for_request_authenticated_superuser(self):
        request = self.factory.get('/')
        request.user = self.superuser
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertIn(self.internal_layer, layers)
        self.assertIn(self.login_required_layer, layers)
        self.assertIn(self.internal_login_required_layer, layers)
        self.assertIn(self.layer_only_for_group, layers)

    @patch('webservice.models.settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', True)
    def test_for_request_unauthenticated_show_layers_only_when_accessible(self):
        class MockUnAuthenticatedUser:
            is_authenticated = False

        request = self.factory.get('/')
        request.user = MockUnAuthenticatedUser()
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertNotIn(self.internal_layer, layers)
        self.assertNotIn(self.login_required_layer, layers)
        self.assertNotIn(self.internal_login_required_layer, layers)
        self.assertNotIn(self.layer_only_for_group, layers)

    @patch('webservice.models.settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', False)
    @patch('webservice.models.is_internal', return_value=False)
    def test_for_request_unauthenticated(self, _):
        class MockUnAuthenticatedUser:
            is_authenticated = False

        request = self.factory.get('/')
        request.user = MockUnAuthenticatedUser()
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertNotIn(self.internal_layer, layers)
        self.assertIn(self.login_required_layer, layers)
        self.assertNotIn(self.internal_login_required_layer, layers)
        self.assertNotIn(self.layer_only_for_group, layers)

    @patch('webservice.models.settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', False)
    @patch('webservice.models.is_internal', return_value=True)
    def test_for_authenticated_request_internal(self, _):
        class MockUnAuthenticatedUser:
            is_authenticated = False

        request = self.factory.get('/')
        request.user = MockUnAuthenticatedUser()
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertIn(self.internal_layer, layers)
        self.assertIn(self.login_required_layer, layers)
        self.assertIn(self.internal_login_required_layer, layers)
        self.assertNotIn(self.layer_only_for_group, layers)

    @patch('webservice.models.settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', True)
    @patch('webservice.models.is_internal', return_value=False)
    def test_for_authenticated_request_external(self, _):
        request = self.factory.get('/')
        request.user = self.user
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertNotIn(self.internal_layer, layers)
        self.assertIn(self.login_required_layer, layers)
        self.assertNotIn(self.internal_login_required_layer, layers)
        self.assertNotIn(self.layer_only_for_group, layers)

    @patch('webservice.models.settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', True)
    @patch('webservice.models.is_internal', return_value=False)
    def test_layer_only_for_group_authorized(self, _):
        request = self.factory.get('/')
        request.user = self.user_with_group
        layers = Layer.authorized.for_request(request)
        self.assertTrue(layers.exists())
        self.assertIn(self.public_layer, layers)
        self.assertNotIn(self.internal_layer, layers)
        self.assertIn(self.login_required_layer, layers)
        self.assertNotIn(self.internal_login_required_layer, layers)
        self.assertIn(self.layer_only_for_group, layers)
