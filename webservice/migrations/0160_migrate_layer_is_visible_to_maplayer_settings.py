from django.db import migrations


def migrate_layer_is_visible_to_maplayer_settings(apps, schema_editor):
    """Copy Layer.is_visible values into MapLayer.settings.

    Existing MapLayer settings that already define is_visible are preserved so
    map-specific visibility settings are not overwritten.
    """
    MapLayer = apps.get_model('webservice', 'MapLayer')

    for map_layer in MapLayer.objects.select_related('layer').all():
        settings = dict(map_layer.settings or {})

        if 'is_visible' in settings:
            continue

        settings['is_visible'] = map_layer.layer.is_visible
        map_layer.settings = settings
        map_layer.save(update_fields=['settings'])


class Migration(migrations.Migration):
    """Move default visibility from Layer to MapLayer settings.

    Layer.is_visible used to define default visibility globally for every use of a
    layer. This migration stores that value per MapLayer instead, so each map can
    decide whether a configured layer is visible by default.
    """
    dependencies = [
        ('webservice', '0159_migrate_layer_is_base_to_maplayer_settings'),
    ]

    operations = [
        migrations.RunPython(
            migrate_layer_is_visible_to_maplayer_settings,
        ),
        migrations.RemoveField(
            model_name='layer',
            name='is_visible',
        ),
    ]
