from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from user_management.models import AtlasGroup
from webservice.audit_events import (
    create_audit_event,
    get_admin_url,
    get_audited_models,
    get_display_value,
    get_group_action_id,
    get_historical_label,
    get_normalized_value,
    is_audited_model,
)
from webservice.models import AuditEvent, Layer, Metadataset, Source


class AuditEventTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="administrator",
            email="administrator@example.com",
            password="password",
        )

    def test_all_configured_models_are_auditable(self):
        """Check that every model in the audit registry has history enabled.

        This protects new models from being listed without producing history.
        """
        audited_models = get_audited_models()

        self.assertTrue(audited_models)
        for model in audited_models:
            with self.subTest(model=model._meta.label_lower):
                self.assertTrue(is_audited_model(model))
                self.assertTrue(hasattr(model, "history"))

        self.assertFalse(is_audited_model(AuditEvent))

    def test_group_changes_are_logged(self):
        """Change an Atlas group and check that it creates an audit event.

        Groups use the normal audit flow, even though they are not maps, layers, or tables.
        """
        group = AtlasGroup(name="Original group")
        group._history_user = self.admin_user
        group.save()

        group.name = "Renamed group"
        group._history_user = self.admin_user
        group.save()

        event = AuditEvent.objects.get(
            source_model="user_management.atlasgroup",
            source_history_id=group.history.latest().history_id,
        )

        self.assertEqual(event.subject_model, "user_management.atlasgroup")
        self.assertEqual(event.object_label, "Renamed group")
        self.assertEqual(event.action_id, "~")
        self.assertIn("Groep\nOriginal group → Renamed group", event.details)

    def test_related_objects_are_logged_with_their_names(self):
        """Show the old and new metadataset names instead of their database ids."""
        first_metadataset = Metadataset.objects.create(title="First dataset", status="completed")
        second_metadataset = Metadataset.objects.create(title="Second dataset", status="completed")
        layer = Layer.objects.create(title="Test layer", metadataset=first_metadataset)

        layer.metadataset = second_metadataset
        layer._history_user = self.admin_user
        layer.save()

        event = AuditEvent.objects.get(
            source_model="webservice.layer",
            source_history_id=layer.history.latest().history_id,
        )

        self.assertIn("Metadataset\nFirst dataset → Second dataset", event.details)

    def test_read_groups_are_logged_with_group_names(self):
        """Show a group name and the read-groups label when layer groups change."""
        group = AtlasGroup.objects.create(name="Editors")
        layer = Layer.objects.create(title="Test layer")

        layer.atlas_groups.add(group)

        event = AuditEvent.objects.filter(source_model="webservice.layer").latest("id")

        self.assertIn("Leesgroepen\n– → Editors", event.details)

    def test_write_groups_are_logged_with_group_names(self):
        """Show a group name and the write-groups label when layer write groups change."""
        group = AtlasGroup.objects.create(name="Editors")
        layer = Layer.objects.create(title="Test layer")

        layer.atlas_write_groups.add(group)

        event = AuditEvent.objects.filter(source_model="webservice.layer").latest("id")

        self.assertIn("Schrijfgroepen\n– → Editors", event.details)

    def test_related_object_uses_its_current_name_without_history(self):
        """Use a related object's current title when no old history exists yet."""
        metadataset = Metadataset.objects.create(title="Dataset without history", status="completed")
        metadataset.history.all().delete()

        label = get_historical_label(Metadataset, metadataset.id, timezone.now())

        self.assertEqual(label, "Dataset without history")

    def test_creating_an_event_twice_does_not_duplicate_it(self):
        """Handle the same source history record twice and keep one audit event.

        This protects the audit log when a history signal is delivered more than once.
        """
        source = Source(title="Test source", url="https://example.com")
        source._history_user = self.admin_user
        source.save()

        event, created = create_audit_event(source.history.latest(), source)

        self.assertFalse(created)
        self.assertEqual(AuditEvent.objects.filter(source_model="webservice.source").count(), 1)
        self.assertEqual(event.source_history_id, source.history.latest().history_id)

    def test_group_action_keeps_creation_and_deletion_actions(self):
        """Keep create and delete as the main action of a grouped event.

        Later changes in the same request must not turn a create or delete into a normal change.
        """
        scenarios = (
            ("+", "~", "+"),
            ("-", "~", "-"),
            ("~", "+", "~"),
            ("~", "~", "~"),
        )

        for current_action, new_action, expected_action in scenarios:
            with self.subTest(current_action=current_action, new_action=new_action):
                self.assertEqual(get_group_action_id(current_action, new_action), expected_action)

    def test_display_helpers_normalize_empty_values(self):
        """Show empty values as a dash and keep normal values readable.

        These helpers are used for every changed field shown in the audit log.
        """

        self.assertIsNone(get_normalized_value(""))
        self.assertIsNone(get_normalized_value(None))
        self.assertEqual(get_display_value(None), "–")
        self.assertEqual(get_display_value("Text"), "Text")

    def test_admin_urls_match_the_audit_subject_action(self):
        """Return an edit link for active objects and none for deleted objects.

        A deleted object cannot safely link to an edit page.
        """
        self.assertEqual(get_admin_url("webservice.source", 12, "~"), "/sources/update/12")
        self.assertIsNone(get_admin_url("webservice.source", 12, "-"))
        self.assertIsNone(get_admin_url("unknown.model", 12, "~"))
