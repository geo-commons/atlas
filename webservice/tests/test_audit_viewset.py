from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from webservice.audit import AuditLogViewSet
from webservice.models import Source


class AuditLogViewSetTests(TestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = get_user_model().objects.create_superuser(
            username="administrator",
            email="administrator@example.com",
            password="password",
        )
        self.factory = APIRequestFactory()

    def test_lists_changes_with_actor_and_changed_fields(self):
        source = Source(title="Original source", url="https://example.com")
        source._history_user = self.admin_user
        source.save()

        source.title = "Renamed source"
        source._history_user = self.admin_user
        source.save()

        request = self.factory.get("/atlas/api/v1/audit-logs/", {"action": "~", "object_id": source.id})
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

        entry = response.data["results"][0]
        self.assertEqual(entry["model"], "Bron")
        self.assertEqual(entry["object"], "Renamed source")
        self.assertEqual(entry["admin_url"], f"/sources/update/{source.id}")
        self.assertEqual(entry["action"], "Gewijzigd")
        self.assertEqual(entry["actor"], "administrator@example.com")
        self.assertIn("Titel\nOriginal source → Renamed source", entry["details"])
