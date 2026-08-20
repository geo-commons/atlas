from django.db import migrations


def migrate_layer_is_base_to_maplayer_settings(apps, schema_editor):
    """Copy Layer.is_base values into MapLayer.settings.

    Only MapLayer rows whose related Layer was marked as a base layer need to be
    updated. Existing custom settings are preserved; missing base-layer values
    are added without overwriting explicitly configured values.
    """
    MapLayer = apps.get_model('webservice', 'MapLayer')

    for map_layer in MapLayer.objects.select_related('layer').filter(layer__is_base=True):
        settings = dict(map_layer.settings or {})

        if settings.get('customSettings'):
            settings.setdefault('is_base', True)
            settings.setdefault('is_visible', map_layer.layer.is_visible)
        else:
            settings.update({
                'customSettings': True,
                'is_base': True,
                'is_visible': map_layer.layer.is_visible,
            })

        map_layer.settings = settings
        map_layer.save(update_fields=['settings'])


class Migration(migrations.Migration):
    """Move base-layer configuration from Layer to MapLayer settings.

    Layer.is_base used to define base-layer behavior globally for every use of a
    layer. This migration stores that value per MapLayer instead, so each map can
    decide whether a configured layer behaves as a base layer.
    """
    dependencies = [
        ('webservice', '0158_remove_layer_published'),
    ]

    operations = [
        migrations.RunPython(
            migrate_layer_is_base_to_maplayer_settings,
        ),
        migrations.RemoveField(
            model_name='layer',
            name='is_base',
        ),
    ]
