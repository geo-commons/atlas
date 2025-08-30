import json
from unittest.mock import patch, Mock

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory

from authz.viewsets import AuthorizeViewSet
from webservice.models import Source
from webservice.tests.utils import create_test_user, create_test_source, create_test_layer


class AuthorizeViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AuthorizeViewSet.as_view({'post': 'list'})
        self.user = create_test_user()
        self.source = create_test_source(source_type=Source.SOURCE_OWS)
        self.layer = create_test_layer()

    def make_request(self, data, user=None):
        request = self.factory.post(
            '/', data=json.dumps(data), content_type='application/json')
        request.user = user or self.user
        return request

    def make_raw_request(self, raw_data, user=None):
        request = self.factory.post(
            '/', data=raw_data, content_type='application/json')
        request.user = user or self.user
        return request

    def base_request_data(self, **overrides):
        data = {
            'source': 'testsource',
            'resource': 'testlayer',
            'request': 'GetFeature',
            'ip': '127.0.0.1',
            'user_agent': 'test-agent',
            'params': {},
        }
        data.update(overrides)
        return data

    def mock_authorization_rule(self, access=False, mutate=False):
        rule = Mock()
        rule.is_accessible_by.return_value = access
        rule.is_mutable_by.return_value = mutate
        rule.audit_log = False
        rule.response_filter = None
        return rule

    def mock_layer_rule(self, access=False, mutate=False):
        layer = Mock()
        layer.is_accessible_by.return_value = access
        layer.is_mutable_by.return_value = mutate
        return layer

    def mock_prefetch_return(self, mock_filter, return_list):
        qs = Mock()
        qs.prefetch_related.return_value = return_list
        mock_filter.return_value = qs

    def test_invalid_json(self):
        request = self.make_raw_request("invalid json")
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('unable to decode json', response.content.decode())

    def test_missing_source_field(self):
        request = self.make_request({})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('source is not defined', response.content.decode())

    @patch('authz.viewsets.Source.objects.get')
    def test_source_not_found(self, mock_get):
        mock_get.side_effect = Source.DoesNotExist
        request = self.make_request({'source': 'test-not-found'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('could not find source with slug',
                      response.content.decode())

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.can_access_source')
    def test_unauthorized_access_as_authenticated_user(self, mock_access, mock_get):
        mock_get.return_value = self.source
        mock_access.return_value = False
        request = self.make_request({'source': 'testsource'})
        response = self.view(request)
        self.assertEqual(response.status_code, 403)

    @patch('authz.viewsets.Source.objects.get')
    def test_authorization_missing_resource_in_data(self, mock_get):
        mock_get.return_value = self.source

        for source_type in [Source.SOURCE_OWS, Source.SOURCE_WMTS, Source.SOURCE_REST]:
            with self.subTest(source_type=source_type):
                self.source.source_type = source_type
                request = self.make_request({'source': 'valid-source'})
                response = self.view(request)
                self.assertEqual(response.status_code, 400)
                self.assertIn('resource is not specified',
                              response.content.decode())

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.Authorization.objects.filter')
    def test_authorization_user_has_read_access_on_authorization_rule(self, mock_auth_filter, mock_get):
        mock_get.return_value = self.source

        for source_type in [Source.SOURCE_OWS, Source.SOURCE_WMTS, Source.SOURCE_REST]:
            with self.subTest(source_type=source_type):
                self.source.source_type = source_type
                self.mock_prefetch_return(
                    mock_auth_filter, [self.mock_authorization_rule(access=True)])
                request = self.make_request(self.base_request_data())
                response = self.view(request)
                self.assertEqual(response.status_code, 200)
                self.assertJSONEqual(response.content, {
                                     'result': True, 'status': 200, 'username': 'testuser'
                                     })

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.Authorization.objects.filter')
    def test_ows_authorization_user_has_mutation_access_on_authorization_rule_for_transaction_request(self, mock_auth_filter, mock_get):
        mock_get.return_value = self.source
        self.source.source_type = Source.SOURCE_OWS
        self.mock_prefetch_return(
            mock_auth_filter, [self.mock_authorization_rule(mutate=True, access=True)])
        request = self.make_request(
            self.base_request_data(request='Transaction'))
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'result': True, 'status': 200, 'username': 'testuser'})

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.Authorization.objects.filter')
    def test_ows_authorization_user_has_no_mutation_access_on_authorization_rule_without_transaction_request(self, mock_auth_filter, mock_get):
        mock_get.return_value = self.source
        self.source.source_type = Source.SOURCE_OWS
        self.mock_prefetch_return(
            mock_auth_filter, [self.mock_authorization_rule(mutate=True)])
        request = self.make_request(
            self.base_request_data(request='RandomTestRequest'))
        response = self.view(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn('does not have access to layer',
                      response.content.decode())

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.Authorization.objects.filter')
    def test_authorization_user_has_no_access_on_authorization_rule(self, mock_auth_filter, mock_get):
        mock_get.return_value = self.source

        for source_type in [Source.SOURCE_OWS, Source.SOURCE_WMTS, Source.SOURCE_REST]:
            with self.subTest(source_type=source_type):
                self.source.source_type = source_type
                self.mock_prefetch_return(
                    mock_auth_filter, [self.mock_authorization_rule()])
                request = self.make_request(self.base_request_data())
                response = self.view(request)
                self.assertEqual(response.status_code, 403)
                self.assertIn('does not have access to',
                              response.content.decode())

    @patch('authz.lib.Layer.objects.filter')
    @patch('authz.viewsets.Authorization.objects.filter')
    @patch('authz.viewsets.Source.objects.get')
    def test_ows_and_wmts_authorization_user_has_layer_read_access(self, mock_get, mock_auth_filter, mock_layer_model):
        mock_get.return_value = self.source

        for source_type in [Source.SOURCE_OWS, Source.SOURCE_WMTS]:
            with self.subTest(source_type=source_type):
                self.source.source_type = source_type
                self.mock_prefetch_return(mock_auth_filter, [])
                self.mock_prefetch_return(
                    mock_layer_model, [self.mock_layer_rule(access=True)])
                request = self.make_request(self.base_request_data())
                response = self.view(request)
                self.assertEqual(response.status_code, 200)
                self.assertJSONEqual(response.content, {
                                     'result': True, 'status': 200, 'username': 'testuser'})

    @patch('authz.lib.Layer.objects.filter')
    @patch('authz.viewsets.Authorization.objects.filter')
    @patch('authz.viewsets.Source.objects.get')
    def test_ows_and_wmts_authorization_user_has_no_layer_read_access(self, mock_get, mock_auth_filter, mock_layer_model):
        mock_get.return_value = self.source

        for source_type in [Source.SOURCE_OWS, Source.SOURCE_WMTS]:
            with self.subTest(source_type=source_type):
                self.source.source_type = source_type
                self.mock_prefetch_return(mock_auth_filter, [])
                self.mock_prefetch_return(
                    mock_layer_model, [self.mock_layer_rule()])
                request = self.make_request(self.base_request_data())
                response = self.view(request)
                self.assertEqual(response.status_code, 403)
                self.assertIn('does not have access to layer',
                              response.content.decode())

    @patch('authz.lib.Layer.objects.filter')
    @patch('authz.viewsets.Authorization.objects.filter')
    @patch('authz.viewsets.Source.objects.get')
    def test_ows_authorization_user_has_layer_mutation_access(self, mock_get, mock_auth_filter, mock_layer_model):
        self.source.source_type = Source.SOURCE_OWS
        mock_get.return_value = self.source
        self.mock_prefetch_return(mock_auth_filter, [])
        self.mock_prefetch_return(
            mock_layer_model, [self.mock_layer_rule(mutate=True, access=True)])
        request = self.make_request(
            self.base_request_data(request='Transaction'))
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'result': True, 'status': 200, 'username': 'testuser'})

    @patch('authz.lib.Layer.objects.filter')
    @patch('authz.viewsets.Authorization.objects.filter')
    @patch('authz.viewsets.Source.objects.get')
    def test_ows_authorization_user_has_no_layer_mutation_access(self, mock_get, mock_auth_filter, mock_layer_model):
        self.source.source_type = Source.SOURCE_OWS
        mock_get.return_value = self.source
        self.mock_prefetch_return(mock_auth_filter, [])
        self.mock_prefetch_return(mock_layer_model, [self.mock_layer_rule()])
        request = self.make_request(
            self.base_request_data(request='Transaction'))
        response = self.view(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn('does not have access to layer',
                      response.content.decode())

    @patch('authz.lib.Layer.objects.filter')
    @patch('authz.viewsets.Authorization.objects.filter')
    @patch('authz.viewsets.Source.objects.get')
    def test_ows_authorization_user_has_no_layer_mutation_access_without_transaction_request(self, mock_get, mock_auth_filter, mock_layer_model):
        self.source.source_type = Source.SOURCE_OWS
        mock_get.return_value = self.source
        self.mock_prefetch_return(mock_auth_filter, [])
        self.mock_prefetch_return(
            mock_layer_model, [self.mock_layer_rule(mutate=True)])
        request = self.make_request(
            self.base_request_data(request='RandomTestRequest'))
        response = self.view(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn('does not have access to layer',
                      response.content.decode())

    @patch('authz.viewsets.Source.objects.get')
    @patch('authz.viewsets.can_access_source')
    def test_authorized_access_as_authenticated_user_with_invalid_source_type(self, mock_access, mock_get):
        mock_get.return_value = self.source
        mock_access.return_value = True
        self.source.source_type = "testsourcetype"
        self.source.save()
        request = self.make_request({'source': 'testsource'})
        response = self.view(request)
        self.assertEqual(response.status_code, 500)
