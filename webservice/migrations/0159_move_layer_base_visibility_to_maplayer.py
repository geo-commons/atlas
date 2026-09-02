from django.db import migrations, models


def migrate_layer_base_visibility_to_maplayer(apps, schema_editor):
    """Move Layer base-layer and visibility defaults to MapLayer fields.

    Existing MapLayer.settings values win when present, so map-specific values
    configured before this migration are preserved while these options stop
    being stored as layer-setting overrides.
    """
    MapLayer = apps.get_model('webservice', 'MapLayer')

    for map_layer in MapLayer.objects.select_related('layer').all():
        settings = dict(map_layer.settings or {})
        map_layer.is_base = settings.pop('is_base', map_layer.layer.is_base)
        map_layer.is_visible = settings.pop('is_visible', map_layer.layer.is_visible)
        map_layer.settings = settings
        map_layer.save(update_fields=['settings', 'is_base', 'is_visible'])


class Migration(migrations.Migration):
    """Move base-layer configuration and visibility from Layer to MapLayer.

    Layer.is_base and Layer.is_visible used to define behavior globally for every
    use of a layer. Store them per MapLayer instead, so each map can decide how a
    configured layer behaves without treating those values as layer-setting
    overrides.
    """
    dependencies = [
        ('webservice', '0158_remove_layer_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='is_base',
            field=models.BooleanField(default=False, verbose_name='Is een basislaag'),
        ),
        migrations.AddField(
            model_name='maplayer',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='Kaartlaag standaard zichtbaar'),
        ),
        migrations.RunPython(
            migrate_layer_base_visibility_to_maplayer,
        ),
        migrations.RemoveField(
            model_name='layer',
            name='is_base',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='is_visible',
        ),
    ]
