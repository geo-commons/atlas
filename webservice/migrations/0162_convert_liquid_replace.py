"""Convert saved replace calls to LiquidJS filter syntax."""

import re

from django.db import migrations


# Match a text argument in single or double quotes, including escaped quotes.
QUOTED_ARGUMENT = r"""(?:'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")"""
# Match old replace filters and replaceAll method calls with two text arguments.
LEGACY_REPLACE_CALL = re.compile(
    rf"(?:\s*\|\s*replace(?:All)?|\.replaceAll)\s*\(\s*"
    rf"({QUOTED_ARGUMENT})\s*,\s*({QUOTED_ARGUMENT})\s*\)"
)
# Leave text outside {{ ... }} unchanged.
LIQUID_OUTPUT_EXPRESSION = re.compile(r"{{.*?}}", re.DOTALL)


def convert_legacy_replace_call(replace_call_match: re.Match[str]) -> str:
    """Keep both text arguments and use the LiquidJS replace filter.

    Args:
        replace_call_match: A match for an old replace call.

    Returns:
        The same call in LiquidJS filter syntax.

    """
    return f" | replace: {replace_call_match[1]}, {replace_call_match[2]}"


def convert_output_expression(expression_match: re.Match[str]) -> str:
    """Change old replace calls inside one {{ ... }} expression.

    Args:
        expression_match: A match for one template expression.

    Returns:
        The expression with LiquidJS replace filters.

    """
    return LEGACY_REPLACE_CALL.sub(convert_legacy_replace_call, expression_match[0])


def convert_legacy_replace_in_value(value: object) -> object:
    """Change old replace calls in text, lists, and JSON objects.

    Args:
        value: A saved field value that may contain templates.

    Returns:
        The value with LiquidJS filters, if any old calls were found.

    """
    if isinstance(value, str):
        return LIQUID_OUTPUT_EXPRESSION.sub(convert_output_expression, value)
    if isinstance(value, list):
        return [convert_legacy_replace_in_value(item) for item in value]
    if isinstance(value, dict):
        return {key: convert_legacy_replace_in_value(item) for key, item in value.items()}
    return value


def convert_saved_replace_filters(apps, schema_editor) -> None:
    """Update saved templates that use the old replace syntax.

    Args:
        apps: The model registry for this migration.
        schema_editor: The editor that gives access to the database connection.

    """
    model_template_fields = (
        ('table', 'Table', (
            'list_endpoint', 'detail_endpoint', 'request_body', 'template_fields',
            'list_template_fields', 'list_cql_filters', 'detail_cql_filters',
        )),
        ('tables', 'Table', ('endpoint', 'error_template', 'list_fields')),
        ('webservice', 'Layer', ('templated_properties',)),
        ('webservice', 'Template', ('endpoint', 'fields', 'template')),
        ('webservice', 'Viewer', ('url',)),
        ('webservice', 'MapLayer', ('settings',)),
    )
    database_alias = schema_editor.connection.alias

    for app_label, model_name, field_names in model_template_fields:
        template_model = apps.get_model(app_label, model_name)
        for record in template_model.objects.using(database_alias).iterator():
            changed_fields = []
            for field_name in field_names:
                original_value = getattr(record, field_name)
                converted_value = convert_legacy_replace_in_value(original_value)
                if converted_value != original_value:
                    setattr(record, field_name, converted_value)
                    changed_fields.append(field_name)
            if changed_fields:
                record.save(update_fields=changed_fields, using=database_alias)


class Migration(migrations.Migration):
    """Run the data migration after the related models exist."""

    dependencies = [
        ('table', '0008_layertotable_ordering_tabletotable_ordering'),
        ('tables', '0020_remove_table_thumbnail'),
        ('webservice', '0161_layer_is_clustered'),
    ]

    operations = [
        migrations.RunPython(convert_saved_replace_filters, migrations.RunPython.noop),
    ]
