from collections import defaultdict

from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

MAXIMUM_PROTECTED_OBJECTS_PER_TYPE = 10


def get_protected_object_label(protected_object):
    """Return a human-readable label for an object preventing deletion."""
    for field_name in ('title', 'name', 'label', 'resource', 'slug'):
        value = getattr(protected_object, field_name, None)
        if value:
            return str(value)

    if hasattr(protected_object, 'from_layer') and hasattr(protected_object, 'to_table'):
        return f'{protected_object.from_layer} → {protected_object.to_table}'

    if hasattr(protected_object, 'from_table') and hasattr(protected_object, 'to_table'):
        return f'{protected_object.from_table} → {protected_object.to_table}'

    return str(protected_object)


def get_protected_object_groups(protected_objects):
    """Group protected objects by type and limit the response to a readable size."""
    objects_by_type = defaultdict(list)
    for protected_object in protected_objects:
        object_type = str(protected_object._meta.verbose_name_plural)
        objects_by_type[object_type].append(protected_object)

    groups = []
    for object_type in sorted(objects_by_type):
        protected_objects_for_type = sorted(
            objects_by_type[object_type],
            key=lambda protected_object: get_protected_object_label(protected_object).lower(),
        )
        visible_objects = protected_objects_for_type[:MAXIMUM_PROTECTED_OBJECTS_PER_TYPE]
        groups.append({
            'type': object_type,
            'objects': [
                {'id': protected_object.pk, 'label': get_protected_object_label(protected_object)}
                for protected_object in visible_objects
            ],
            'remaining_count': len(protected_objects_for_type) - len(visible_objects),
        })

    return groups


def get_protected_object_detail(protected_object_groups):
    """Create the detail shown directly in existing API error notifications."""
    object_type_details = []
    for group in protected_object_groups:
        labels = [protected_object['label'] for protected_object in group['objects']]
        if group['remaining_count']:
            labels.append(f"en nog {group['remaining_count']} andere")
        object_type_details.append(f"{group['type']}: {', '.join(labels)}")

    return '. '.join(object_type_details)


def api_exception_handler(exc, context):
    """Return a useful API response when a referenced object is deleted."""
    if not isinstance(exc, ProtectedError):
        return exception_handler(exc, context)

    protected_object_groups = get_protected_object_groups(exc.protected_objects)
    protected_by = [group['type'] for group in protected_object_groups]
    protected_by_text = get_protected_object_detail(protected_object_groups)
    detail = 'Dit object kan niet worden verwijderd, omdat het nog wordt gebruikt.'
    if protected_by_text:
        detail = f'{detail} Verwijder of koppel eerst de volgende onderdelen los: {protected_by_text}.'

    return Response(
        {
            'detail': detail,
            'code': 'protected_delete',
            'protected_by': protected_by,
            'protected_objects': protected_object_groups,
        },
        status=status.HTTP_409_CONFLICT,
    )
