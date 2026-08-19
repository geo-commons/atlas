from django.db import migrations


def migrate_layer_is_visible_to_maplayer_settings(apps, schema_editor):
    MapLayer = apps.get_model('webservice', 'MapLayer')

    for map_layer in MapLayer.objects.select_related('layer').all():
        settings = dict(map_layer.settings or {})

        if 'is_visible' in settings:
            continue

        settings['is_visible'] = map_layer.layer.is_visible
        map_layer.settings = settings
        map_layer.save(update_fields=['settings'])


def restore_layer_is_visible_from_maplayer_settings(apps, schema_editor):
    Layer = apps.get_model('webservice', 'Layer')
    MapLayer = apps.get_model('webservice', 'MapLayer')

    visible_layer_ids = (
        MapLayer.objects.filter(settings__is_visible=True)
        .values_list('layer_id', flat=True)
        .distinct()
    )
    Layer.objects.filter(id__in=visible_layer_ids).update(is_visible=True)


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0159_migrate_layer_is_base_to_maplayer_settings'),
    ]

    operations = [
        migrations.RunPython(
            migrate_layer_is_visible_to_maplayer_settings,
            restore_layer_is_visible_from_maplayer_settings,
        ),
        migrations.RemoveField(
            model_name='layer',
            name='is_visible',
        ),
    ]
