from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from webservice.audit import AuditLogViewSet, get_audited_models
from webservice.models import AuditEvent, Category, Layer, Map, MapCategory, MapLayer, Source
from webservice.serializers import MapSerializer


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

    def test_supports_drf_search_syntax(self):
        source = Source(title="Original source", url="https://example.com")
        source._history_user = self.admin_user
        source.save()

        source.title = "Renamed source"
        source._history_user = self.admin_user
        source.save()

        request = self.factory.get("/atlas/api/v1/audit-logs/", {"search": '"Renamed source"'})
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["object"], "Renamed source")

    def test_shows_map_layer_changes_as_map_changes(self):
        map_instance = Map(title="Test map")
        map_instance._history_user = self.admin_user
        map_instance.save()
        layer = Layer.objects.create(title="Road works")

        map_layer = MapLayer(map=map_instance, layer=layer, settings={})
        map_layer._history_user = self.admin_user
        map_layer.save()

        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {"model": "webservice.map", "search": "Road works"},
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        entry = response.data["results"][0]
        self.assertEqual(entry["model"], "Kaart")
        self.assertEqual(entry["object"], "Test map")
        self.assertEqual(entry["admin_url"], f"/maps/update/{map_instance.id}")
        self.assertEqual(entry["action"], "Gewijzigd")
        self.assertEqual(entry["details"], "Kaartlaag toegevoegd\nRoad works")

    def test_shows_map_categories_as_map_changes(self):
        audited_models = get_audited_models()

        self.assertIn(MapCategory, audited_models)
        self.assertIn(MapLayer, audited_models)

    def test_unique_fields_only_contains_user_facing_model_labels(self):
        request = self.factory.get("/atlas/api/v1/audit-logs/unique-fields/")
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "unique_fields"})(request)

        self.assertEqual(response.status_code, 200)
        models = {model["id"]: model["label"] for model in response.data["models"]}

        self.assertEqual(models["webservice.layer"], "Kaartlaag")
        self.assertEqual(models["webservice.map"], "Kaart")
        self.assertNotIn("webservice.maplayer", models)
        self.assertNotIn("webservice.mapcategory", models)

    def test_shows_map_category_creation_as_a_map_change(self):
        map_instance = Map.objects.create(title="Test map")
        category = Category.objects.create(title="Road works")
        map_category = MapCategory(map=map_instance, category=category)
        map_category._history_user = self.admin_user
        map_category.save()

        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {"model": "webservice.map", "object_id": map_instance.id, "search": "Categorie toegevoegd"},
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["details"], "Categorie toegevoegd\nRoad works")

    def test_uses_category_names_and_friendly_labels_for_map_layer_changes(self):
        map_instance = Map.objects.create(title="Test map")
        layer = Layer.objects.create(title="Road works")
        category = Category.objects.create(title="Road works")
        map_category = MapCategory.objects.create(map=map_instance, category=category)
        map_layer = MapLayer.objects.create(map=map_instance, layer=layer, settings={})

        map_layer.map_category = map_category
        map_layer.ordering = 1
        map_layer._history_user = self.admin_user
        map_layer.save()

        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {"model": "webservice.map", "object_id": map_instance.id, "action": "~"},
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        details = [entry["details"] for entry in response.data["results"]]
        self.assertIn("Categorie\nGeen categorie → Road works", details[0])
        self.assertIn("Positie\n0 → 1", details[0])

    def test_map_serializer_adds_category_and_layer_audit_entries(self):
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        category = Category.objects.create(title="Road works")
        layer = Layer.objects.create(title="Road works", layer_type=category)

        serializer = MapSerializer(
            map_instance,
            data={
                "title": "Test map",
                "slug": "test-map",
                "categories": [{"category": category.id, "ordering": 0}],
                "layers": [{"layer": layer.id, "settings": {}, "ordering": 0}],
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        entries = self.get_map_audit_entries(map_instance)
        details = {entry["details"] for entry in entries}

        self.assertIn("Categorie toegevoegd\nRoad works", details)
        self.assertIn("Kaartlaag toegevoegd\nRoad works", details)

    def test_map_serializer_removes_layer_audit_entry(self):
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        category = Category.objects.create(title="Road works")
        map_category = MapCategory.objects.create(map=map_instance, category=category)
        layer = Layer.objects.create(title="Road works", layer_type=category)
        MapLayer.objects.create(map=map_instance, layer=layer, map_category=map_category, settings={})

        serializer = MapSerializer(
            map_instance,
            data={
                "title": "Test map",
                "slug": "test-map",
                "categories": [{"category": category.id, "ordering": 0}],
                "layers": [],
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        details = {entry["details"] for entry in self.get_map_audit_entries(map_instance)}

        self.assertIn("Kaartlaag verwijderd\nRoad works", details)

    def test_map_serializer_removes_category_audit_entry(self):
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        category = Category.objects.create(title="Road works")
        MapCategory.objects.create(map=map_instance, category=category)

        serializer = MapSerializer(
            map_instance,
            data={
                "title": "Test map",
                "slug": "test-map",
                "categories": [],
                "layers": [],
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        details = {entry["details"] for entry in self.get_map_audit_entries(map_instance)}

        self.assertIn("Categorie verwijderd\nRoad works", details)

    def test_map_serializer_only_logs_changed_map_fields(self):
        map_instance = Map.objects.create(title="Test map", slug="custom-map-url")
        map_instance._history_user = self.admin_user

        serializer = MapSerializer(
            map_instance,
            data={
                "title": "Test map",
                "slug": "custom-map-url",
                "description": "Updated description",
            },
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        entries = self.get_map_audit_entries(map_instance)

        self.assertEqual(len(entries), 1)
        self.assertIn("Beschrijving van de kaart\n– → Updated description", entries[0]["details"])
        self.assertNotIn("Kort kenmerk", entries[0]["details"])

    def test_map_layer_audit_event_keeps_the_original_layer_name(self):
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        layer = Layer.objects.create(title="Original layer")
        MapLayer.objects.create(map=map_instance, layer=layer, settings={})

        layer.title = "Renamed layer"
        layer.save()

        audit_event = AuditEvent.objects.get(source_model="webservice.maplayer")

        self.assertEqual(audit_event.object_label, "Test map")
        self.assertEqual(audit_event.details, "Kaartlaag toegevoegd\nOriginal layer")

    def get_map_audit_entries(self, map_instance):
        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {"model": "webservice.map", "object_id": map_instance.id, "action": "~", "page_size": 100},
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        return response.data["results"]
