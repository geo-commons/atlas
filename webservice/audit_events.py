from dataclasses import dataclass
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from simple_history.models import HistoricalRecords

from authz.models import Authorization
from table.models import LayerToTable, Table as LegacyTable, TableToTable
from tables.models import Table
from user_management.models import AtlasGroup, AtlasUser
from webservice.models import (
    AuditEvent,
    AuditEventGroup,
    Category,
    Layer,
    Map,
    MapCategory,
    MapLayer,
    Metadataset,
    Source,
    Viewer,
)


ACTION_LABELS = {
    "+": "Aangemaakt",
    "~": "Gewijzigd",
    "-": "Verwijderd",
}

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

HIDDEN_FIELD_NAMES = {"api_key", "last_login", "password", "secret", "token"}
MAP_LAYER_MODEL_LABEL = "webservice.maplayer"
MAP_CATEGORY_MODEL_LABEL = "webservice.mapcategory"
TABLE_TO_TABLE_MODEL_LABEL = "table.tabletotable"
LAYER_TO_TABLE_MODEL_LABEL = "table.layertotable"


@dataclass
class AuditChange:
    """Represent a visible field change between two historical records."""

    field_name: str
    field_label: str
    old_value: object
    new_value: object


def get_audited_models():
    """Return models whose history should appear in the Atlas audit log."""
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
        LegacyTable,
        TableToTable,
        LayerToTable,
        Viewer,
    )


def is_audited_model(model):
    """Return whether a model is configured to produce audit events."""
    return model in get_audited_models()


def create_audit_event(history_record, source_instance=None):
    """Create and group an audit event for a newly created history record."""
    if not is_audited_model(history_record.instance_type):
        return None

    event_data = get_audit_event_data(history_record, source_instance)
    if event_data is None:
        return None

    # History signals can be delivered more than once while fixtures or migrations
    # are replayed. The source history row is the stable idempotency key.
    audit_event, created = AuditEvent.objects.get_or_create(
        source_model=event_data["source_model"],
        source_history_id=event_data["source_history_id"],
        defaults=event_data,
    )
    if audit_event.group_id is None:
        audit_event.group = get_audit_event_group(event_data)
        audit_event.save(update_fields=["group"])
        update_audit_event_group(audit_event.group, audit_event)

    return audit_event, created


def get_audit_event_group(event_data):
    """Return the group for an event in the current request."""
    request_id = get_request_id()
    if request_id is None:
        # Changes without a request cannot be grouped with other events.
        return AuditEventGroup.objects.create(**get_audit_event_group_data(event_data))

    group_data = get_audit_event_group_data(event_data)
    group, created = AuditEventGroup.objects.get_or_create(
        request_id=request_id,
        subject_model=event_data["subject_model"],
        object_id=event_data["object_id"],
        defaults=group_data,
    )
    return group


def get_audit_event_group_data(event_data):
    """Build the initial persisted fields for an audit-event group."""
    return {
        "request_id": get_request_id(),
        "event_date": event_data["event_date"],
        "subject_model": event_data["subject_model"],
        "subject_label": event_data["subject_label"],
        "object_id": event_data["object_id"],
        "object_label": event_data["object_label"],
        "action_id": event_data["action_id"],
        "actor": event_data["actor"],
        "actor_label": event_data["actor_label"],
        "details": "",
        "changes": [],
        "admin_url": event_data["admin_url"],
    }


def update_audit_event_group(group, audit_event):
    """Merge an event's timestamp, action, and changes into its group."""
    group.event_date = max(group.event_date, audit_event.event_date)
    group.action_id = get_group_action_id(group.action_id, audit_event.action_id)
    group.details = "\n\n".join(filter(None, [group.details, audit_event.details]))
    group.changes = [*group.changes, *audit_event.changes]
    group.save(update_fields=["event_date", "action_id", "details", "changes"])


def get_group_action_id(current_action_id, new_action_id):
    """Determine the group action after adding another event."""
    if current_action_id in {"+", "-"}:
        return current_action_id
    if current_action_id == new_action_id:
        return current_action_id
    return "~"


def get_request_id():
    """Return the current request identifier when audit grouping is enabled."""
    request = getattr(HistoricalRecords.context, "request", None)
    return getattr(request, "audit_event_request_id", None)


def get_audit_event_data(history_record, source_instance=None):
    """Build the immutable audit-event payload from a historical record."""
    source_model = history_record.instance_type
    source_model_label = source_model._meta.label_lower
    subject_model, subject_label, object_id, object_label = get_subject_data(
        history_record,
        source_instance,
    )
    action_id = get_action_id(source_model_label, history_record.history_type)
    audit_content = get_audit_content(history_record, source_instance)
    if audit_content is None:
        return None

    details, changes = audit_content

    return {
        "source_model": source_model_label,
        "source_history_id": history_record.history_id,
        "event_date": history_record.history_date,
        "subject_model": subject_model,
        "subject_label": subject_label,
        "object_id": object_id,
        "object_label": object_label,
        "action_id": action_id,
        "actor": history_record.history_user,
        "actor_label": get_actor_label(history_record.history_user),
        "details": details,
        "changes": changes,
        "admin_url": get_admin_url(subject_model, object_id, action_id),
    }


def get_subject_data(history_record, source_instance):
    """Return the admin object that should own a history record in the log."""
    source_model_label = history_record.instance_type._meta.label_lower
    if source_model_label not in {MAP_LAYER_MODEL_LABEL, MAP_CATEGORY_MODEL_LABEL}:
        if source_model_label == TABLE_TO_TABLE_MODEL_LABEL:
            return get_table_relation_subject_data(history_record, source_instance)
        if source_model_label == LAYER_TO_TABLE_MODEL_LABEL:
            return get_layer_relation_subject_data(history_record, source_instance)
        return (
            source_model_label,
            history_record.instance_type._meta.verbose_name.title(),
            history_record.id,
            get_historical_object_label(history_record),
        )

    map_id = history_record.map_id
    return (
        "webservice.map",
        "Kaart",
        map_id,
        get_related_object_label(source_instance, "map", map_id, Map, history_record.history_date),
    )


def get_table_relation_subject_data(history_record, source_instance):
    """Return the source table as the subject of a table-to-table relation event."""
    table_id = history_record.from_table_id
    return (
        "table.table",
        "Tabel",
        table_id,
        get_related_object_label(source_instance, "from_table", table_id, LegacyTable, history_record.history_date),
    )


def get_layer_relation_subject_data(history_record, source_instance):
    """Return the source layer as the subject of a layer-to-table relation event."""
    layer_id = history_record.from_layer_id
    return (
        "webservice.layer",
        "Kaartlaag",
        layer_id,
        get_related_object_label(source_instance, "from_layer", layer_id, Layer, history_record.history_date),
    )


def get_action_id(source_model_label, history_type):
    """Map a history action to the action displayed for its audit subject."""
    if source_model_label in {MAP_LAYER_MODEL_LABEL, MAP_CATEGORY_MODEL_LABEL}:
        return "~"
    return history_type


def get_audit_content(history_record, source_instance=None):
    """Return a legacy text summary and structured changes for one history record."""
    source_model_label = history_record.instance_type._meta.label_lower
    if source_model_label == MAP_LAYER_MODEL_LABEL:
        return get_map_layer_audit_content(history_record, source_instance)
    if source_model_label == MAP_CATEGORY_MODEL_LABEL:
        return get_map_category_audit_content(history_record, source_instance)
    if source_model_label == TABLE_TO_TABLE_MODEL_LABEL:
        return get_table_relation_audit_content(history_record, source_instance)
    if source_model_label == LAYER_TO_TABLE_MODEL_LABEL:
        return get_layer_relation_audit_content(history_record, source_instance)

    if history_record.history_type == "+":
        return "Nieuw object", [{"value": "Nieuw object"}]
    if history_record.history_type == "-":
        return "Object verwijderd", [{"value": "Object verwijderd"}]

    changes = get_changes(history_record)
    if not changes:
        return None

    return "\n".join(format_change(change) for change in changes), [get_change_detail(change) for change in changes]


def get_map_layer_audit_content(history_record, source_instance):
    """Describe a map-layer relationship change in terms of its map and layer."""
    layer_name = get_related_object_label(
        source_instance,
        "layer",
        history_record.layer_id,
        Layer,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        details = f"Kaartlaag toegevoegd\n{layer_name}"
        return details, [{"value": details}]
    if history_record.history_type == "-":
        details = f"Kaartlaag verwijderd\n{layer_name}"
        return details, [{"value": details}]

    changes = get_changes(history_record)
    if not changes:
        return None

    formatted_changes = "\n".join(format_map_layer_change(change, history_record) for change in changes)
    return (
        f"Kaartlaag gewijzigd\n{layer_name}\n{formatted_changes}",
        [get_map_layer_change_detail(change, history_record, layer_name) for change in changes],
    )


def get_map_category_audit_content(history_record, source_instance):
    """Describe a map-category relationship change in terms of its map and category."""
    category_name = get_related_object_label(
        source_instance,
        "category",
        history_record.category_id,
        Category,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        details = f"Categorie toegevoegd\n{category_name}"
        return details, [{"value": details}]
    if history_record.history_type == "-":
        details = f"Categorie verwijderd\n{category_name}"
        return details, [{"value": details}]

    changes = get_changes(history_record)
    if not changes:
        return None

    formatted_changes = "\n".join(format_map_category_change(change) for change in changes)
    return (
        f"Categorie gewijzigd\n{category_name}\n{formatted_changes}",
        [get_map_category_change_detail(change, category_name) for change in changes],
    )


def get_table_relation_audit_content(history_record, source_instance):
    """Describe a relation added to, removed from, or changed on a legacy table."""
    table_name = get_related_object_label(
        source_instance,
        "to_table",
        history_record.to_table_id,
        LegacyTable,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        details = f"Gerelateerde tabel toegevoegd\n{table_name}"
        return details, [{"value": details}]
    if history_record.history_type == "-":
        details = f"Gerelateerde tabel verwijderd\n{table_name}"
        return details, [{"value": details}]

    changes = get_changes(history_record)
    if not changes:
        return None
    return (
        f"Gerelateerde tabel gewijzigd\n{table_name}\n" + "\n".join(format_change(change) for change in changes),
        [get_change_detail(change, table_name) for change in changes],
    )


def get_layer_relation_audit_content(history_record, source_instance):
    """Describe a table relation added to, removed from, or changed on a layer."""
    table_name = get_related_object_label(
        source_instance,
        "to_table",
        history_record.to_table_id,
        LegacyTable,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        details = f"Tabel gekoppeld\n{table_name}"
        return details, [{"value": details}]
    if history_record.history_type == "-":
        details = f"Tabel ontkoppeld\n{table_name}"
        return details, [{"value": details}]

    changes = get_changes(history_record)
    if not changes:
        return None
    return (
        f"Tabelkoppeling gewijzigd\n{table_name}\n" + "\n".join(format_change(change) for change in changes),
        [get_change_detail(change, table_name) for change in changes],
    )


def get_changes(history_record):
    """Return meaningful, non-sensitive field changes from the previous history record."""
    previous_record = history_record.prev_record
    if previous_record is None:
        return []

    source_model_label = history_record.instance_type._meta.label_lower
    changes = []
    for change in history_record.diff_against(previous_record).changes:
        if change.field.casefold() in HIDDEN_FIELD_NAMES:
            continue
        if get_normalized_value(change.old) == get_normalized_value(change.new):
            continue

        field = history_record.instance_type._meta.get_field(change.field)
        old_value = change.old
        new_value = change.new
        if not (source_model_label == MAP_LAYER_MODEL_LABEL and change.field == "map_category"):
            old_value = get_change_value(change.old, field, history_record.history_date)
            new_value = get_change_value(change.new, field, history_record.history_date)

        changes.append(
            AuditChange(
                field_name=change.field,
                field_label=str(field.verbose_name).capitalize(),
                old_value=old_value,
                new_value=new_value,
            )
        )

    return changes


def format_change(change):
    """Format one field change for display in the audit log."""
    return f"{change.field_label}\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"


def get_change_detail(change, related_object_label=None):
    """Build one structured change that remains safe for multiline values."""
    field = change.field_label
    if related_object_label is not None:
        field = f"{related_object_label} · {field}"
    return {
        "field": field,
        "old_value": get_display_value(change.old_value),
        "new_value": get_display_value(change.new_value),
    }


def get_change_value(value, field, history_date):
    """Return a readable value for a changed model field."""
    if get_normalized_value(value) is None:
        return value

    if field.many_to_one:
        return get_historical_label(field.related_model, value, history_date)

    if field.many_to_many and isinstance(value, list):
        return get_many_to_many_labels(value, field.related_model, history_date)

    return value


def get_many_to_many_labels(values, related_model, history_date):
    """Return readable labels for the related objects in a history M2M value."""
    related_id_field = related_model._meta.model_name
    labels = []
    for value in values:
        if not isinstance(value, dict):
            continue

        related_id = value.get(related_id_field)
        if related_id is not None:
            labels.append(get_historical_label(related_model, related_id, history_date))

    return ", ".join(labels)


def get_display_value(value):
    """Normalize and render a field value for the audit log."""
    normalized_value = get_normalized_value(value)
    text = "–" if normalized_value is None else str(normalized_value)
    return text


def get_normalized_value(value):
    """Treat empty strings and null values as the same empty audit value."""
    if value in (None, ""):
        return None
    if isinstance(value, Decimal):
        return str(value)
    return value


def format_map_layer_change(change, history_record):
    """Use map-layer-specific labels for category and ordering changes."""
    if change.field_name == "map_category":
        old_category = get_map_category_label(change.old_value, history_record.history_date)
        new_category = get_map_category_label(change.new_value, history_record.history_date)
        return f"Categorie\n{old_category} → {new_category}"
    if change.field_name == "ordering":
        return f"Positie\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"
    return format_change(change)


def get_map_layer_change_detail(change, history_record, layer_name):
    """Build a structured map-layer change with its friendly field labels."""
    if change.field_name == "map_category":
        return {
            "field": f"{layer_name} · Categorie",
            "old_value": get_map_category_label(change.old_value, history_record.history_date),
            "new_value": get_map_category_label(change.new_value, history_record.history_date),
        }
    if change.field_name == "ordering":
        return get_change_detail(
            AuditChange("ordering", "Positie", change.old_value, change.new_value),
            layer_name,
        )
    return get_change_detail(change, layer_name)


def format_map_category_change(change):
    """Use the user-facing position label for map-category ordering changes."""
    if change.field_name == "ordering":
        return f"Positie\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"
    return format_change(change)


def get_map_category_change_detail(change, category_name):
    """Build a structured map-category change with its friendly position label."""
    if change.field_name == "ordering":
        return get_change_detail(
            AuditChange("ordering", "Positie", change.old_value, change.new_value),
            category_name,
        )
    return get_change_detail(change, category_name)


def get_map_category_label(map_category_id, history_date):
    """Resolve a map-category id to its category label at a point in time."""
    if map_category_id is None:
        return "Geen categorie"

    map_category_history = MapCategory.history.filter(
        id=map_category_id,
        history_date__lte=history_date,
    ).order_by("-history_date", "-history_id").first()
    if map_category_history is None:
        return "Onbekende categorie"

    return get_historical_label(Category, map_category_history.category_id, history_date)


def get_related_object_label(source_instance, field_name, object_id, model, history_date):
    """Return a related object's label from the instance or its historical record."""
    if source_instance is not None:
        try:
            return str(getattr(source_instance, field_name))
        except ObjectDoesNotExist:
            pass

    # Relations may already be gone (especially during cascaded deletes). Look
    # up the latest value available at the event time to keep the audit text
    # historically accurate instead of using the current database state.
    return get_historical_label(model, object_id, history_date)


def get_historical_label(model, object_id, history_date):
    """Return an object's last known label at or before a historical timestamp."""
    history_record = model.history.filter(
        id=object_id,
        history_date__lte=history_date,
    ).order_by("-history_date", "-history_id").first()
    if history_record is None:
        current_object = model._default_manager.filter(id=object_id).first()
        if current_object is not None:
            return get_object_label(current_object)
        return f"ID {object_id}"

    return get_historical_object_label(history_record)


def get_historical_object_label(history_record):
    """Select the most useful human-readable label from a history record."""
    return get_object_label(history_record)


def get_object_label(instance):
    """Select the most useful human-readable label from a model instance."""
    for field_name in ("title", "name", "label", "username", "resource"):
        value = getattr(instance, field_name, None)
        if value:
            return str(value)
    return f"ID {instance.id}"


def get_actor_label(actor):
    """Return the user-facing name for an actor or the system actor."""
    if actor is None:
        return "Systeem"
    return actor.name or actor.email or actor.get_username()


def get_admin_url(subject_model, object_id, action_id):
    """Return the edit URL for a non-deleted audit subject when one exists."""
    if action_id == "-":
        return None

    path_template = ADMIN_OBJECT_PATHS.get(subject_model)
    return path_template.format(id=object_id) if path_template else None
