from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from simple_history.models import HistoricalRecords

from table.models import LayerToTable, Table, TableToTable
from table.serializers import TableSerializer
from webservice.audit import AuditLogViewSet
from webservice.middleware import AuditEventRequestMiddleware
from webservice.models import AuditEvent, AuditEventGroup, Category, Layer, Map, MapCategory, MapLayer, Source
from webservice.serializers import LayerCreateUpdateSerializer, MapSerializer


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
        """Change a source and return its actor, changed field, and edit link."""
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
        self.assertEqual(entry["summary"], "2 wijzigingen")

    def test_denies_non_super_user(self):
        """Block a staff user without superuser rights from reading audit logs."""
        staff_user = get_user_model().objects.create_user(
            username="staff-user",
            email="staff-user@example.com",
            password="password",
            is_staff=True,
        )
        request = self.factory.get("/atlas/api/v1/audit-logs/")
        force_authenticate(request, user=staff_user)

        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 403)

    def test_shows_map_layer_changes_as_map_changes(self):
        """Add a layer to a map and show the event on the map, not the relation."""
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

    def test_unique_fields_only_contains_user_facing_model_labels(self):
        """Return readable filter labels and hide internal relation model names."""
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
        """Add a category to a map and show the event in the map history."""
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
        """Show category names and readable labels when a map layer changes."""
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
        """Save a map with a category and layer, then log both additions."""
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

    def test_map_mutations_in_one_request_are_grouped(self):
        """Save a category and layer in one map request as one audit entry."""
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        category = Category.objects.create(title="Road works")
        layer = Layer.objects.create(title="Road works", layer_type=category)
        request = self.factory.put("/atlas/api/v1/maps/")
        request.user = self.admin_user
        request.audit_event_request_id = "00000000-0000-0000-0000-000000000001"

        HistoricalRecords.context.request = request
        try:
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
        finally:
            del HistoricalRecords.context.request

        entries = self.get_map_audit_entries(map_instance)

        self.assertEqual(len(entries), 1)
        self.assertIn("Categorie toegevoegd\nRoad works", entries[0]["details"])
        self.assertIn("Kaartlaag toegevoegd\nRoad works", entries[0]["details"])
        self.assertEqual(entries[0]["summary"], "2 wijzigingen")

    def test_map_serializer_removes_layer_audit_entry(self):
        """Remove a layer through the map serializer and log that removal."""
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
        """Remove a category through the map serializer and log that removal."""
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
        """Update one map field and do not log fields with the same value."""
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
        """Keep the original layer name after the layer is renamed later."""
        map_instance = Map.objects.create(title="Test map", slug="test-map")
        layer = Layer.objects.create(title="Original layer")
        MapLayer.objects.create(map=map_instance, layer=layer, settings={})

        layer.title = "Renamed layer"
        layer.save()

        audit_event = AuditEvent.objects.get(source_model="webservice.maplayer")

        self.assertEqual(audit_event.object_label, "Test map")
        self.assertEqual(audit_event.details, "Kaartlaag toegevoegd\nOriginal layer")

    def test_assigns_a_group_identifier_to_every_request(self):
        """Give each request a different id so events cannot cross group."""
        middleware = AuditEventRequestMiddleware(lambda request: None)
        map_request = self.factory.patch("/atlas/api/v1/maps/1/")
        layer_request = self.factory.patch("/atlas/api/v1/layers/1/")

        middleware(map_request)
        middleware(layer_request)

        self.assertTrue(hasattr(map_request, "audit_event_request_id"))
        self.assertTrue(hasattr(layer_request, "audit_event_request_id"))
        self.assertNotEqual(map_request.audit_event_request_id, layer_request.audit_event_request_id)

    def test_layer_mutations_in_one_request_are_grouped(self):
        """Move two layer table relations in one request and create one log entry."""
        source = Source.objects.create(title="Test source", url="https://example.com")
        layer = Layer.objects.create(title="Test layer")
        first_table = Table.objects.create(title="First table", source=source)
        second_table = Table.objects.create(title="Second table", source=source)
        first_relation = LayerToTable.objects.create(from_layer=layer, to_table=first_table, field_mapping={}, ordering=0)
        second_relation = LayerToTable.objects.create(from_layer=layer, to_table=second_table, field_mapping={}, ordering=1)
        request = self.factory.patch(f"/atlas/api/v1/layers/{layer.id}/")
        request.user = self.admin_user
        AuditEventRequestMiddleware(lambda request: None)(request)

        HistoricalRecords.context.request = request
        try:
            serializer = LayerCreateUpdateSerializer(
                layer,
                data={
                    "related_tables": [
                        {"id": first_relation.id, "to_table": first_table.id, "field_mapping": {}, "ordering": 1},
                        {"id": second_relation.id, "to_table": second_table.id, "field_mapping": {}, "ordering": 0},
                    ]
                },
                partial=True,
            )
            self.assertTrue(serializer.is_valid(), serializer.errors)
            serializer.save()
        finally:
            del HistoricalRecords.context.request

        groups = AuditEventGroup.objects.filter(
            request_id=request.audit_event_request_id,
            subject_model="webservice.layer",
            object_id=layer.id,
        )

        self.assertEqual(groups.count(), 1)
        self.assertIn("Tabelkoppeling gewijzigd\nFirst table\nVolgorde\n0 → 1", groups[0].details)
        self.assertIn("Tabelkoppeling gewijzigd\nSecond table\nVolgorde\n1 → 0", groups[0].details)

    def test_table_mutations_in_one_request_are_grouped(self):
        """Move two table relations in one request and create one log entry."""
        source = Source.objects.create(title="Test source", url="https://example.com")
        table = Table.objects.create(title="Source table", source=source)
        first_table = Table.objects.create(title="First table", source=source)
        second_table = Table.objects.create(title="Second table", source=source)
        first_relation = TableToTable.objects.create(from_table=table, to_table=first_table, field_mapping={}, ordering=0)
        second_relation = TableToTable.objects.create(from_table=table, to_table=second_table, field_mapping={}, ordering=1)
        request = self.factory.patch(f"/atlas/api/v1/tables/{table.id}/")
        request.user = self.admin_user
        AuditEventRequestMiddleware(lambda request: None)(request)

        HistoricalRecords.context.request = request
        try:
            serializer = TableSerializer(
                table,
                data={
                    "related_tables": [
                        {"id": first_relation.id, "to_table": first_table.id, "field_mapping": {}, "ordering": 1},
                        {"id": second_relation.id, "to_table": second_table.id, "field_mapping": {}, "ordering": 0},
                    ]
                },
                partial=True,
                context={"request": request},
            )
            self.assertTrue(serializer.is_valid(), serializer.errors)
            serializer.save()
        finally:
            del HistoricalRecords.context.request

        groups = AuditEventGroup.objects.filter(
            request_id=request.audit_event_request_id,
            subject_model="table.table",
            object_id=table.id,
        )

        self.assertEqual(groups.count(), 1)
        self.assertIn("Gerelateerde tabel gewijzigd\nFirst table\nVolgorde\n0 → 1", groups[0].details)
        self.assertIn("Gerelateerde tabel gewijzigd\nSecond table\nVolgorde\n1 → 0", groups[0].details)

    def test_table_relationship_changes_are_audited(self):
        """Create a table relation and log it on the source table."""
        source = Source.objects.create(title="Test source", url="https://example.com")
        table = Table.objects.create(title="Source table", source=source)
        related_table = Table.objects.create(title="Related table", source=source)
        TableToTable.objects.create(from_table=table, to_table=related_table, field_mapping={})

        audit_event = AuditEvent.objects.get(source_model="table.tabletotable")

        self.assertEqual(audit_event.subject_model, "table.table")
        self.assertEqual(audit_event.object_label, "Source table")
        self.assertEqual(audit_event.details, "Gerelateerde tabel toegevoegd\nRelated table")

    def test_table_relationship_update_is_logged_once_with_its_changed_field(self):
        """Change one relation field and create one event with that field."""
        source = Source.objects.create(title="Test source", url="https://example.com")
        table = Table.objects.create(title="Source table", source=source)
        related_table = Table.objects.create(title="Related table", source=source)
        relation = TableToTable.objects.create(from_table=table, to_table=related_table, field_mapping={})

        relation.ordering = 2
        relation._history_user = self.admin_user
        relation.save()

        events = AuditEvent.objects.filter(source_model="table.tabletotable").order_by("event_date", "id")

        self.assertEqual(events.count(), 2)
        self.assertEqual(events.last().action_id, "~")
        self.assertEqual(
            events.last().details,
            "Gerelateerde tabel gewijzigd\nRelated table\nVolgorde\n0 → 2",
        )

    def test_layer_table_relationship_changes_are_logged_on_the_layer(self):
        """Add and remove a table relation and log both events on the layer."""
        source = Source.objects.create(title="Test source", url="https://example.com")
        related_table = Table.objects.create(title="Related table", source=source)
        layer = Layer.objects.create(title="Source layer")
        relation = LayerToTable.objects.create(from_layer=layer, to_table=related_table, field_mapping={})

        relation.delete()

        events = AuditEvent.objects.filter(source_model="table.layertotable").order_by("event_date", "id")

        self.assertEqual(events.count(), 2)
        self.assertEqual(events.first().subject_model, "webservice.layer")
        self.assertEqual(events.first().object_label, "Source layer")
        self.assertEqual(events.first().details, "Tabel gekoppeld\nRelated table")
        self.assertEqual(events.last().action_id, "-")
        self.assertEqual(events.last().details, "Tabel ontkoppeld\nRelated table")

    def test_filters_multiple_object_ids(self):
        """Filter changed sources by multiple object ids, model, action, and actor."""
        first_source = Source(title="First source", url="https://example.com/first")
        first_source._history_user = self.admin_user
        first_source.save()
        second_source = Source(title="Second source", url="https://example.com/second")
        second_source._history_user = self.admin_user
        second_source.save()

        first_source.title = "First source renamed"
        first_source._history_user = self.admin_user
        first_source.save()
        second_source.title = "Second source renamed"
        second_source._history_user = self.admin_user
        second_source.save()

        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {
                "model": "webservice.source",
                "object_id": f"{first_source.id},{second_source.id}",
                "action": "~",
                "actor": self.admin_user.id,
            },
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(
            {entry["object"] for entry in response.data["results"]},
            {"First source renamed", "Second source renamed"},
        )

    def get_map_audit_entries(self, map_instance):
        request = self.factory.get(
            "/atlas/api/v1/audit-logs/",
            {"model": "webservice.map", "object_id": map_instance.id, "action": "~", "page_size": 100},
        )
        force_authenticate(request, user=self.admin_user)
        response = AuditLogViewSet.as_view({"get": "list"})(request)

        self.assertEqual(response.status_code, 200)
        return response.data["results"]
