from dataclasses import dataclass

from django.core.exceptions import ObjectDoesNotExist

from authz.models import Authorization
from table.models import Table as LegacyTable
from tables.models import Table
from user_management.models import AtlasGroup, AtlasUser
from webservice.models import AuditEvent, Category, Layer, Map, MapCategory, MapLayer, Metadataset, Source, Viewer


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


@dataclass
class AuditChange:
    field_name: str
    field_label: str
    old_value: object
    new_value: object


def get_audited_models():
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
        Viewer,
    )


def is_audited_model(model):
    return model in get_audited_models()


def create_audit_event(history_record, source_instance=None):
    if not is_audited_model(history_record.instance_type):
        return None

    event_data = get_audit_event_data(history_record, source_instance)
    if event_data is None:
        return None

    return AuditEvent.objects.get_or_create(
        source_model=event_data["source_model"],
        source_history_id=event_data["source_history_id"],
        defaults=event_data,
    )


def get_audit_event_data(history_record, source_instance=None):
    source_model = history_record.instance_type
    source_model_label = source_model._meta.label_lower
    subject_model, subject_label, object_id, object_label = get_subject_data(
        history_record,
        source_instance,
    )
    action_id = get_action_id(source_model_label, history_record.history_type)
    details = get_change_summary(history_record, source_instance)
    if details is None:
        return None

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
        "admin_url": get_admin_url(subject_model, object_id, action_id),
    }


def get_subject_data(history_record, source_instance):
    source_model_label = history_record.instance_type._meta.label_lower
    if source_model_label not in {MAP_LAYER_MODEL_LABEL, MAP_CATEGORY_MODEL_LABEL}:
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


def get_action_id(source_model_label, history_type):
    if source_model_label in {MAP_LAYER_MODEL_LABEL, MAP_CATEGORY_MODEL_LABEL}:
        return "~"
    return history_type


def get_change_summary(history_record, source_instance):
    source_model_label = history_record.instance_type._meta.label_lower
    if source_model_label == MAP_LAYER_MODEL_LABEL:
        return get_map_layer_change_summary(history_record, source_instance)
    if source_model_label == MAP_CATEGORY_MODEL_LABEL:
        return get_map_category_change_summary(history_record, source_instance)

    if history_record.history_type == "+":
        return "Nieuw object"
    if history_record.history_type == "-":
        return "Object verwijderd"

    changes = get_changes(history_record)
    if not changes:
        return None

    return "\n".join(format_change(change) for change in changes)


def get_map_layer_change_summary(history_record, source_instance):
    layer_name = get_related_object_label(
        source_instance,
        "layer",
        history_record.layer_id,
        Layer,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        return f"Kaartlaag toegevoegd\n{layer_name}"
    if history_record.history_type == "-":
        return f"Kaartlaag verwijderd\n{layer_name}"

    changes = get_changes(history_record)
    if not changes:
        return None

    formatted_changes = "\n".join(format_map_layer_change(change, history_record) for change in changes)
    return f"Kaartlaag gewijzigd\n{layer_name}\n{formatted_changes}"


def get_map_category_change_summary(history_record, source_instance):
    category_name = get_related_object_label(
        source_instance,
        "category",
        history_record.category_id,
        Category,
        history_record.history_date,
    )
    if history_record.history_type == "+":
        return f"Categorie toegevoegd\n{category_name}"
    if history_record.history_type == "-":
        return f"Categorie verwijderd\n{category_name}"

    changes = get_changes(history_record)
    if not changes:
        return None

    formatted_changes = "\n".join(format_map_category_change(change) for change in changes)
    return f"Categorie gewijzigd\n{category_name}\n{formatted_changes}"


def get_changes(history_record):
    previous_record = history_record.prev_record
    if previous_record is None:
        return []

    changes = []
    for change in history_record.diff_against(previous_record).changes:
        if change.field.casefold() in HIDDEN_FIELD_NAMES:
            continue

        field = history_record.instance_type._meta.get_field(change.field)
        changes.append(
            AuditChange(
                field_name=change.field,
                field_label=str(field.verbose_name),
                old_value=change.old,
                new_value=change.new,
            )
        )

    return changes


def format_change(change):
    return f"{change.field_label}\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"


def get_display_value(value):
    text = "–" if value in (None, "") else str(value)
    return f"{text[:117]}..." if len(text) > 120 else text


def format_map_layer_change(change, history_record):
    if change.field_name == "map_category":
        old_category = get_map_category_label(change.old_value, history_record.history_date)
        new_category = get_map_category_label(change.new_value, history_record.history_date)
        return f"Categorie\n{old_category} → {new_category}"
    if change.field_name == "ordering":
        return f"Positie\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"
    return format_change(change)


def format_map_category_change(change):
    if change.field_name == "ordering":
        return f"Positie\n{get_display_value(change.old_value)} → {get_display_value(change.new_value)}"
    return format_change(change)


def get_map_category_label(map_category_id, history_date):
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
    if source_instance is not None:
        try:
            return str(getattr(source_instance, field_name))
        except ObjectDoesNotExist:
            pass

    return get_historical_label(model, object_id, history_date)


def get_historical_label(model, object_id, history_date):
    history_record = model.history.filter(
        id=object_id,
        history_date__lte=history_date,
    ).order_by("-history_date", "-history_id").first()
    if history_record is None:
        return "Onbekend object"

    return get_historical_object_label(history_record)


def get_historical_object_label(history_record):
    for field_name in ("title", "name", "label", "username", "resource"):
        value = getattr(history_record, field_name, None)
        if value:
            return str(value)
    return f"ID {history_record.id}"


def get_actor_label(actor):
    if actor is None:
        return "Systeem"
    return actor.name or actor.email or actor.get_username()


def get_admin_url(subject_model, object_id, action_id):
    if action_id == "-":
        return None

    path_template = ADMIN_OBJECT_PATHS.get(subject_model)
    return path_template.format(id=object_id) if path_template else None
