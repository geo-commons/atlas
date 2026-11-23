import re

from django.db import migrations


QUOTED_STRING = r"""(?:'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")"""
REPLACE_CALL = re.compile(
    rf"(?:\s*\|\s*replace(?:All)?|\.replaceAll)\s*\(\s*"
    rf"({QUOTED_STRING})\s*,\s*({QUOTED_STRING})\s*\)"
)
OUTPUT_EXPRESSION = re.compile(r"{{.*?}}", re.DOTALL)


def convert_value(value):
    if isinstance(value, str):
        return OUTPUT_EXPRESSION.sub(
            lambda expression: REPLACE_CALL.sub(
                lambda match: f" | replace: {match[1]}, {match[2]}",
                expression[0],
            ),
            value,
        )
    if isinstance(value, list):
        return [convert_value(item) for item in value]
    if isinstance(value, dict):
        return {key: convert_value(item) for key, item in value.items()}
    return value


def convert_saved_templates(apps, schema_editor):
    template_fields = (
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
    database = schema_editor.connection.alias

    for app_label, model_name, field_names in template_fields:
        model = apps.get_model(app_label, model_name)
        for instance in model.objects.using(database).iterator():
            changed_fields = []
            for field_name in field_names:
                original = getattr(instance, field_name)
                converted = convert_value(original)
                if converted != original:
                    setattr(instance, field_name, converted)
                    changed_fields.append(field_name)
            if changed_fields:
                instance.save(update_fields=changed_fields, using=database)


class Migration(migrations.Migration):
    dependencies = [
        ('table', '0008_layertotable_ordering_tabletotable_ordering'),
        ('tables', '0020_remove_table_thumbnail'),
        ('webservice', '0161_layer_is_clustered'),
    ]

    operations = [
        migrations.RunPython(convert_saved_templates, migrations.RunPython.noop),
    ]
