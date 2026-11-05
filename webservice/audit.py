import django_filters
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from webservice.audit_events import (
    ACTION_LABELS,
    LAYER_TO_TABLE_MODEL_LABEL,
    MAP_CATEGORY_MODEL_LABEL,
    MAP_LAYER_MODEL_LABEL,
    TABLE_TO_TABLE_MODEL_LABEL,
    get_audited_models,
)
from webservice.models import AuditEventGroup
from webservice.pagination import StandardResultsSetPagination
from webservice.permissions import IsAtlasAdmin


class AuditEventFilter(django_filters.FilterSet):
    """Expose the audit-log query parameters as comma-separated filters."""

    model = django_filters.BaseInFilter(field_name="subject_model", lookup_expr="in")
    object_id = django_filters.BaseInFilter(field_name="object_id", lookup_expr="in")
    action = django_filters.BaseInFilter(field_name="action_id", lookup_expr="in")
    actor = django_filters.BaseInFilter(field_name="actor_id", lookup_expr="in")

    class Meta:
        model = AuditEventGroup
        fields = []


class AuditLogViewSet(ReadOnlyModelViewSet):
    """List grouped audit events for Atlas administrators."""

    permission_classes = [IsAtlasAdmin]
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuditEventFilter
    search_fields = ["subject_label", "object_label", "actor_label", "details"]
    ordering_fields = [
        ("event_date", "date"),
        ("subject_label", "model"),
        ("object_label", "object"),
        ("action_id", "action"),
        ("actor_label", "actor"),
    ]
    ordering = ["-event_date", "-id"]

    def get_queryset(self):
        """Return audit groups together with their actor relation."""
        return AuditEventGroup.objects.select_related("actor")

    def list(self, request, *args, **kwargs):
        """Filter, paginate, and serialize the audit-event groups."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response([self.serialize_event(event) for event in page])

        return Response([self.serialize_event(event) for event in queryset])

    @action(detail=False, methods=["get"], url_path="unique-fields")
    def unique_fields(self, request):
        """Return the actor, model, and action options for audit-log filters."""
        events = self.get_queryset()
        actors = {
            event["actor_id"]: event["actor_label"]
            for event in events.exclude(actor_id__isnull=True).values("actor_id", "actor_label").distinct()
        }

        return Response(
            {
                "actors": [{"id": actor_id, "label": label} for actor_id, label in sorted(actors.items())],
                "models": self.get_model_filter_options(),
                "actions": [{"id": action, "label": label} for action, label in ACTION_LABELS.items()],
            }
        )

    @staticmethod
    def get_model_filter_options():
        """Return user-facing model filters, merging relationship events into their parent object."""
        options = {}
        for model in get_audited_models():
            model_id = model._meta.label_lower
            if model_id in {MAP_LAYER_MODEL_LABEL, MAP_CATEGORY_MODEL_LABEL}:
                options["webservice.map"] = {"id": "webservice.map", "label": "Kaart"}
            elif model_id == TABLE_TO_TABLE_MODEL_LABEL:
                options["table.table"] = {"id": "table.table", "label": "Tabel"}
            elif model_id == LAYER_TO_TABLE_MODEL_LABEL:
                options["webservice.layer"] = {"id": "webservice.layer", "label": "Kaartlaag"}
            else:
                options[model_id] = {"id": model_id, "label": model._meta.verbose_name.title()}

        return sorted(options.values(), key=lambda option: option["label"])

    @classmethod
    def serialize_event(cls, event):
        """Convert an audit-event group to the response shape consumed by the admin UI."""
        return {
            "id": event.id,
            "date": event.event_date,
            "model": event.subject_label,
            "model_id": event.subject_model,
            "object": event.object_label,
            "admin_url": event.admin_url,
            "action": ACTION_LABELS[event.action_id],
            "action_id": event.action_id,
            "actor": event.actor_label,
            "actor_id": event.actor_id,
            "details": event.details,
            "changes": event.changes,
            "summary": cls.get_summary(event),
        }

    @staticmethod
    def get_summary(event):
        """Build a compact, user-facing summary of an audit-event group."""
        if event.action_id == "+":
            return "Nieuw object"
        if event.action_id == "-":
            return "Object verwijderd"

        change_count = len(event.changes)
        return f"{change_count} wijziging" if change_count == 1 else f"{change_count} wijzigingen"
