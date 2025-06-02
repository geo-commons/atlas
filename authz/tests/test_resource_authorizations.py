from django.test import TestCase
from unittest.mock import patch, Mock

from django.test.client import RequestFactory

from authz.tests.utils import create_test_authorization
from webservice.tests.utils import create_test_user, create_test_group


class TestResourceReadAuthorizations(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.group = create_test_group()
        self.authorization = create_test_authorization()
        self.factory = RequestFactory()

    @patch('authz.models.is_internal')
    def test_resource_read_authorizations(self, mock_is_internal):
        test_cases = [
            {
                "desc": "Internal resource not accessible by external user",
                "only_internal": True,
                "login_required": False,
                "user_authenticated": False,
                "mock_is_internal": False,
                "expected": False
            },
            {
                "desc": "Public resource accessible by anonymous user",
                "only_internal": False,
                "login_required": False,
                "user_authenticated": False,
                "expected": True
            },
            {
                "desc": "Login required resource not accessible by anonymous user",
                "login_required": True,
                "user_authenticated": False,
                "expected": False
            },
            {
                "desc": "Resource with groups not accessible by anonymous user",
                "user_authenticated": False,
                "resource_groups": [lambda: self.group],
                "expected": False
            },
            {
                "desc": "Resource without groups accessible by authenticated user",
                "user_authenticated": True,
                "expected": True
            },
            {
                "desc": "Resource with groups not accessible by authenticated user without group",
                "user_authenticated": True,
                "resource_groups": [lambda: self.group],
                "user_groups": [],
                "expected": False
            },
            {
                "desc": "Resource with matching group accessible by user",
                "user_authenticated": True,
                "user_groups": [lambda: self.group],
                "resource_groups": [lambda: self.group],
                "expected": True
            },
            {
                "desc": "Resource with different group not accessible by user",
                "user_authenticated": True,
                "user_groups": [lambda: create_test_group("differenttestgroup")],
                "resource_groups": [lambda: self.group],
                "expected": False
            }
        ]

        for case in test_cases:
            with self.subTest(msg=case["desc"]):
                mock_is_internal.return_value = case.get("mock_is_internal", True)
                request = self.factory.get('/')
                user_groups = [g() for g in case.get("user_groups", [])]
                resource_groups = [g() for g in case.get("resource_groups", [])]

                if case["user_authenticated"]:
                    self.user.atlas_groups.set(user_groups)
                    request.user = Mock(is_authenticated=True, atlas_groups=self.user.atlas_groups.all())
                else:
                    request.user = Mock(is_authenticated=False)

                self.authorization.only_internal = case.get("only_internal", False)
                self.authorization.login_required = case.get("login_required", False)
                self.authorization.atlas_groups.set(resource_groups)
                self.authorization.save()

                accessible = self.authorization.is_accessible_by(request.user, request)
                self.assertEqual(accessible, case["expected"])


class TestResourceMutationAuthorizations(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.group = create_test_group()
        self.authorization = create_test_authorization()
        self.factory = RequestFactory()

    @patch('authz.models.is_internal')
    def test_resource_mutation_authorizations(self, mock_is_internal):
        test_cases = [
            {
                "desc": "Internal resource not mutable by external user",
                "mock_is_internal": False,
                "closed_dataset": True,
                "user_authenticated": False,
                "expected": False,
            },
            {
                "desc": "Resource not mutable by non-authenticated user",
                "user_authenticated": False,
                "expected": False,
            },
            {
                "desc": "Resource mutable by authenticated user with authenticated_can_mutate",
                "user_authenticated": True,
                "authenticated_can_mutate": True,
                "expected": True,
            },
            {
                "desc": "Resource without write groups is not mutable by authenticated user",
                "user_authenticated": True,
                "expected": False,
            },
            {
                "desc": "Resource with write groups is mutable by authenticated user with group",
                "user_authenticated": True,
                "user_groups": [lambda: self.group],
                "resource_write_groups": [lambda: self.group],
                "expected": True,
            },
            {
                "desc": "Resource with write groups is not mutable by user with different group",
                "user_authenticated": True,
                "user_groups": [lambda: create_test_group("differenttestgroup")],
                "resource_write_groups": [lambda: self.group],
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

                self.authorization.closed_dataset = case.get("closed_dataset", False)
                self.authorization.authenticated_can_mutate = case.get("authenticated_can_mutate", False)
                self.authorization.atlas_write_groups.set(
                    [g() for g in case.get("resource_write_groups", [])]
                )
                self.authorization.save()

                mutable = self.authorization.is_mutable_by(request.user, request)
                self.assertEqual(mutable, case["expected"])