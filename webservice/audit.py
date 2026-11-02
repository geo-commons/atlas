import heapq

from django.contrib.auth import get_user_model
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from webservice.pagination import StandardResultsSetPagination


HIDDEN_FIELD_NAMES = {"api_key", "last_login", "password", "secret", "token"}

ADMIN_OBJECT_PATHS = {
    "authz.authorization": "/authorizations/update/{id}",
    "table.table": "/tables/update/{id}",
    "tables.table": "/tables_old/update/{id}",
    "user_management.atlasgroup": "/groups/update/{id}",
    "user_management.atlasuser": "/users/update/{id}",
    "webservice.category": "/categories/update/{id}",
    "webservice.layer": "/layers/update/{id}",
    "webservice.map": "/maps/update/{id}",
    "webservice.metadataset": "/metadatasets/update/{id}",
    "webservice.source": "/sources/update/{id}",
    "webservice.viewer": "/viewers/update/{id}",
}


class AuditLogSearchFilter(filters.SearchFilter):
    """Apply DRF's standard search query parameter to merged history entries."""

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset

        return [
            entry
            for entry in queryset
            if all(search_term.casefold() in view.search_value(*entry) for search_term in search_terms)
        ]


class AuditLogMultipleFieldsFilter(filters.BaseFilterBackend):
    """Apply the same comma-separated filters as other Atlas list endpoints."""

    def filter_queryset(self, request, queryset, view):
        model_values = self._values(request, "model")
        object_id_values = self._values(request, "object_id")
        action_values = self._values(request, "action")
        actor_values = self._values(request, "actor")

        return [
            entry
            for entry in queryset
            if self._matches(entry, model_values, object_id_values, action_values, actor_values)
        ]

    @staticmethod
    def _values(request, field):
        value = request.query_params.get(field, "")
        return {item.strip() for item in value.split(",") if item.strip()}

    @staticmethod
    def _matches(entry, model_values, object_id_values, action_values, actor_values):
        _, model, record = entry
        return (
            (not model_values or model._meta.label_lower in model_values)
            and (not object_id_values or str(record.id) in object_id_values)
            and (not action_values or record.history_type in action_values)
            and (not actor_values or str(record.history_user_id) in actor_values)
        )


class AuditLogOrderingFilter(filters.BaseFilterBackend):
    """Apply DRF's standard ordering query parameter to merged history entries."""

    def filter_queryset(self, request, queryset, view):
        requested_fields = request.query_params.get("ordering", "-date").split(",")
        ordering_fields = set(view.ordering_fields)

        for requested_field in reversed(requested_fields):
            descending = requested_field.startswith("-")
            field = requested_field.removeprefix("-")
            if field not in ordering_fields:
                continue
            queryset = sorted(queryset, key=lambda entry: view.ordering_value(field, *entry), reverse=descending)

        return queryset


def get_audited_models():
    """Return the models that can be changed from the Atlas admin interface."""
    from authz.models import Authorization
    from table.models import Table as TableOld
    from tables.models import Table
    from user_management.models import AtlasGroup, AtlasUser
    from webservice.models import Category, Layer, Map, MapCategory, MapLayer, Metadataset, Source, Viewer

    return (
        Authorization,
        AtlasGroup,
        AtlasUser,
        Category,
        Layer,
        Map,
        MapCategory,
        MapLayer,
        Metadataset,
        Source,
        Table,
        TableOld,
        Viewer,
    )


class AuditLogViewSet(GenericViewSet):
    """Expose model history in one chronological, read-only admin log."""

    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [AuditLogSearchFilter, AuditLogMultipleFieldsFilter, AuditLogOrderingFilter]
    search_fields = ["model", "object", "actor", "details"]
    multiple_lookup_fields = ["model", "object_id", "action", "actor"]
    ordering_fields = ["date", "model", "object", "action", "actor"]

    def list(self, request):
        history_querysets = []
        for model in get_audited_models():
            queryset = model.history.all().select_related("history_user").order_by("-history_date")
            history_querysets.append((model, queryset))

        entries = list(
            heapq.merge(
                *(self._history_entries(model, queryset) for model, queryset in history_querysets),
                key=lambda entry: entry[0],
                reverse=True,
            )
        )
        entries = [entry for entry in entries if self._is_visible_entry(*entry)]
        entries = self.filter_queryset(entries)

        page = self.paginate_queryset(entries)
        if page is not None:
            return self.get_paginated_response([self._serialize_entry(model, record) for _, model, record in page])

        return Response([self._serialize_entry(model, record) for _, model, record in entries])

    @action(detail=False, methods=["get"], url_path="unique-fields")
    def unique_fields(self, request):
        actor_ids = set()
        models = []
        for model in get_audited_models():
            models.append({"id": model._meta.label_lower, "label": model._meta.verbose_name.title()})
            actor_ids.update(
                model.history.exclude(history_user_id__isnull=True).values_list("history_user_id", flat=True).distinct()
            )

        users = get_user_model().objects.filter(id__in=actor_ids).order_by("username")
        return Response(
            {
                "actors": [{"id": user.id, "label": self._actor_name(user)} for user in users],
                "models": sorted(models, key=lambda model: model["label"]),
                "actions": [
                    {"id": "+", "label": "Aangemaakt"},
                    {"id": "~", "label": "Gewijzigd"},
                    {"id": "-", "label": "Verwijderd"},
                ],
            }
        )

    @staticmethod
    def _history_entries(model, queryset):
        for record in queryset.iterator():
            yield record.history_date, model, record

    def _serialize_entry(self, model, record):
        action_label = {"+": "Aangemaakt", "~": "Gewijzigd", "-": "Verwijderd"}[record.history_type]
        return {
            "id": f"{model._meta.label_lower}:{record.history_id}",
            "date": record.history_date,
            "model": model._meta.verbose_name.title(),
            "model_id": model._meta.label_lower,
            "object": self._object_name(record),
            "admin_url": self._admin_url(model, record),
            "action": action_label,
            "action_id": record.history_type,
            "actor": self._actor_name(record.history_user),
            "actor_id": record.history_user_id,
            "details": self._change_summary(model, record),
        }

    def search_value(self, _, model, record):
        actor = self._actor_name(record.history_user)
        details = self._change_summary(model, record)
        return " ".join((model._meta.verbose_name, self._object_name(record), actor, details)).casefold()

    def ordering_value(self, field, _, model, record):
        values = {
            "date": record.history_date,
            "model": model._meta.verbose_name,
            "object": self._object_name(record),
            "action": record.history_type,
            "actor": self._actor_name(record.history_user),
        }
        return values[field].casefold() if isinstance(values[field], str) else values[field]

    @staticmethod
    def _actor_name(user):
        if user is None:
            return "Systeem"

        return user.name or user.email or user.get_username()

    @staticmethod
    def _object_name(record):
        for field_name in ("title", "name", "label", "username", "resource"):
            value = getattr(record, field_name, None)
            if value:
                return str(value)
        return f"ID {record.id}"

    @staticmethod
    def _admin_url(model, record):
        if record.history_type == "-":
            return None

        model_label = model._meta.label_lower
        if model_label in {"webservice.mapcategory", "webservice.maplayer"}:
            return f"/maps/update/{record.map_id}"

        path_template = ADMIN_OBJECT_PATHS.get(model_label)
        return path_template.format(id=record.id) if path_template else None

    def _change_summary(self, model, record):
        if record.history_type == "+":
            return "Nieuw object"
        if record.history_type == "-":
            return "Object verwijderd"

        previous_record = record.prev_record
        if previous_record is None:
            return "Object gewijzigd"

        changes = self._changes(model, record, previous_record)

        return "\n".join(self._format_change(change) for change in changes) or "Geen zichtbare veldwijzigingen"

    def _is_visible_entry(self, _, model, record):
        if record.history_type != "~":
            return True

        previous_record = record.prev_record
        return previous_record is not None and bool(self._changes(model, record, previous_record))

    def _changes(self, model, record, previous_record):
        changes = []
        for change in record.diff_against(previous_record).changes:
            if change.field.casefold() in HIDDEN_FIELD_NAMES:
                continue
            field = model._meta.get_field(change.field)
            changes.append(
                {
                    "field": str(field.verbose_name),
                    "old": self._display_value(change.old),
                    "new": self._display_value(change.new),
                }
            )

        return changes

    @staticmethod
    def _format_change(change):
        return f"{change['field']}\n{change['old']} → {change['new']}"

    @staticmethod
    def _display_value(value):
        text = "–" if value in (None, "") else str(value)
        return f"{text[:117]}..." if len(text) > 120 else text
