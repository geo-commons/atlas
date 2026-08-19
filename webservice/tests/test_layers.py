from unittest.mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from constance.test import override_config

from webservice.models import Layer, Category
from webservice.serializers import LayerListSerializer, LayerSerializer
from webservice.tests.utils import create_test_user, create_test_group, create_test_layer


class TestLayerModel(TestCase):
    def setUp(self):
        self.closed_dataset = Layer.objects.create(
            slug="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='theme_layer'))
        self.open_dataset = Layer.objects.create(
            title="Purm",
            layer_name="",
            _popup_attributes="test\ntest1",
            layer_type=Category.objects.create(
                title='base_layer'))

    def test_layer_name(self):
        self.assertEqual(self.closed_dataset.layer_name,
                         "topp:Purm_Stembureaus_2018")

    def test_is_closed_dataset(self):
        self.assertTrue(self.closed_dataset.is_closed_dataset)
        self.assertFalse(self.open_dataset.is_closed_dataset)

    def test_slddiv(self):
        self.assertEqual(self.closed_dataset.slddiv,
                         "sld_div_purm_stembureaus_2018")

    def test_infodiv(self):
        self.assertEqual(self.closed_dataset.infodiv,
                         "info_purm_stembureaus_2018")

    def test_sld(self):
        self.assertEqual(self.closed_dataset.sld, "sld_purm_stembureaus_2018")

    def test_legend(self):
        self.assertEqual(self.closed_dataset.legend,
                         "lgn_purm_stembureaus_2018")

    def test_filterid(self):
        self.assertEqual(self.closed_dataset.filterid,
                         "flt_purm_stembureaus_2018")

    def test_filterdataid(self):
        self.assertEqual(self.closed_dataset.filterdataid,
                         "data_purm_stembureaus_2018")

    def test_datazoekid(self):
        self.assertEqual(self.closed_dataset.datazoekid,
                         "zoek_data_purm_stembureaus_2018")

    def test_params(self):
        self.assertEqual(self.closed_dataset.params,
                         "{'layers': 'topp:Purm_Stembureaus_2018'}")

    def test_source(self):
        self.assertEqual(self.closed_dataset.source, """
source: new ol.source.TileWMS({
    projection: 'EPSG:28992',
    url: '',
    params: {'layers': 'topp:Purm_Stembureaus_2018'},
    serverType: 'geoserver'
})""")


class TestLayerOrdering(TestCase):
    def setUp(self):
        self.stembureaus = Layer.objects.create(
            slug="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            ordering=10)
        self.purm = Layer.objects.create(
            title="Purm",
            layer_name="",
            closed_dataset=False,
            _popup_attributes="test\ntest1",
            ordering=0)
        self.purm2 = Layer.objects.create(
            title="Purm2",
            layer_name="",
            closed_dataset=False,
            _popup_attributes="test\ntest1",
            ordering=0)

    def test_ordering(self):
        layers = list(Layer.objects.all())
        self.assertListEqual(
            [self.purm, self.purm2, self.stembureaus],
            layers)


class TestLayerReadAuthorizations(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.group = create_test_group()
        self.layer = create_test_layer()
        self.factory = RequestFactory()

    @patch('webservice.models.is_internal')
    def test_layer_read_authorizations(self, mock_is_internal):
        test_cases = [
            {
                "desc": "Internal layer not accessible by external user",
                "mock_is_internal": False,
                "closed_dataset": True,
                "user_authenticated": False,
                "expected": False,
            },
            {
                "desc": "Internal layer accessible by external user if feature flag is off",
                "mock_is_internal": False,
                "closed_dataset": True,
                "user_authenticated": False,
                "internal_layer_feature_flag": False,
                "expected": True,
            },
            {
                "desc": "Layer accessible by anonymous user if public and no login required",
                "user_authenticated": False,
                "login_required": False,
                "expected": True,
            },
            {
                "desc": "Layer with login_required not accessible by anonymous user",
                "user_authenticated": False,
                "login_required": True,
                "expected": False,
            },
            {
                "desc": "Layer with groups not accessible by anonymous user",
                "user_authenticated": False,
                "layer_groups": [lambda: self.group],
                "expected": False,
            },
            {
                "desc": "Layer without groups accessible by authenticated user",
                "user_authenticated": True,
                "expected": True,
            },
            {
                "desc": "Layer with groups not accessible by authenticated user without groups",
                "user_authenticated": True,
                "layer_groups": [lambda: self.group],
                "user_groups": [],
                "expected": False,
            },
            {
                "desc": "Layer with groups accessible by authenticated user with same group",
                "user_authenticated": True,
                "user_groups": [lambda: self.group],
                "layer_groups": [lambda: self.group],
                "expected": True,
            },
            {
                "desc": "Layer with groups not accessible by authenticated user with different group",
                "user_authenticated": True,
                "user_groups": [lambda: create_test_group("differenttestgroup")],
                "layer_groups": [lambda: self.group],
                "expected": False,
            },
        ]

        for case in test_cases:
            with self.subTest(msg=case["desc"]):
                mock_is_internal.return_value = case.get("mock_is_internal", True)
                request = self.factory.get('/')

                user_groups = [g() for g in case.get("user_groups", [])]
                if case["user_authenticated"]:
                    self.user.atlas_groups.set(user_groups)
                    request.user = Mock(
                        is_authenticated=True,
                        atlas_groups=self.user.atlas_groups.all()
                    )
                else:
                    request.user = Mock(is_authenticated=False)


                self.layer.closed_dataset = case.get("closed_dataset", False)
                self.layer.login_required = case.get("login_required", False)
                self.layer.atlas_groups.set(
                    [g() for g in case.get("layer_groups", [])]
                )
                self.layer.save()

                internal_layer_feature_flag = case.get("internal_layer_feature_flag", True)
                with override_config(FEATURE_LAYER_INTERNAL_VISIBILITY=internal_layer_feature_flag):
                    accessible = self.layer.is_accessible_by(request.user, request)
                self.assertEqual(accessible, case["expected"])


class TestLayerMutationAuthorizations(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.group = create_test_group()
        self.layer = create_test_layer()
        self.factory = RequestFactory()

    @patch('webservice.models.is_internal')
    def test_layer_mutation_authorizations(self, mock_is_internal):
        test_cases = [
            {
                "desc": "Internal layer not mutable by external user",
                "mock_is_internal": False,
                "closed_dataset": True,
                "user_authenticated": False,
                "expected": False,
            },
            {
                "desc": "Layer not mutable by non-authenticated user",
                "user_authenticated": False,
                "expected": False,
            },
            {
                "desc": "Layer with authenticated_can_mutate is mutable by authenticated user",
                "user_authenticated": True,
                "authenticated_can_mutate": True,
                "expected": True,
            },
            {
                "desc": "Layer without write groups is not mutable by authenticated user",
                "user_authenticated": True,
                "expected": False,
            },
            {
                "desc": "Layer with write groups is mutable by user with matching group",
                "user_authenticated": True,
                "user_groups": [lambda: self.group],
                "layer_write_groups": [lambda: self.group],
                "expected": True,
            },
            {
                "desc": "Layer with write groups not mutable by user with different group",
                "user_authenticated": True,
                "user_groups": [lambda: create_test_group("differenttestgroup")],
                "layer_write_groups": [lambda: self.group],
                "expected": False,
            },
        ]

        for case in test_cases:
            with self.subTest(msg=case["desc"]):
                mock_is_internal.return_value = case.get("mock_is_internal", True)
                request = self.factory.get('/')

                user_groups = [g() for g in case.get("user_groups", [])]
                if case["user_authenticated"]:
                    self.user.atlas_groups.set(user_groups)
                    request.user = Mock(
                        is_authenticated=True,
                        atlas_groups=self.user.atlas_groups.all()
                    )
                else:
                    request.user = Mock(is_authenticated=False)

                self.layer.closed_dataset = case.get("closed_dataset", False)
                self.layer.authenticated_can_mutate = case.get("authenticated_can_mutate", False)
                self.layer.atlas_write_groups.set(
                    [g() for g in case.get("layer_write_groups", [])]
                )
                self.layer.save()

                mutable = self.layer.is_mutable_by(request.user, request)
                self.assertEqual(mutable, case["expected"])
