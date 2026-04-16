from constance import config
from django.db import migrations


def backfill_map_positions(apps, schema_editor):
    Map = apps.get_model('webservice', 'Map')

    default_position = {
        'zoom': config.POSITION_ZOOM,
        'center': {
            'x': config.POSITION_CENTER_X,
            'y': config.POSITION_CENTER_Y,
        },
    }

    for map_instance in Map.objects.all():
        settings = dict(map_instance.settings or {})
        if settings.get('position'):
            continue

        settings['position'] = default_position
        map_instance.settings = settings
        map_instance.save(update_fields=['settings'])


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0151_map_is_main'),
    ]

    operations = [
        migrations.RunPython(backfill_map_positions, migrations.RunPython.noop),
    ]
