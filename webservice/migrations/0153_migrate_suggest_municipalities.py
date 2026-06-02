from django.db import migrations

def _migrate_suggest_municipalities(apps, schema_editor):
    Constance = apps.get_model('constance', 'Constance')
    try:
        old_value = Constance.objects.get(key='SUGGEST_MUNICIPALITIES').value
    except Constance.DoesNotExist:
        return

    Constance.objects.update_or_create(
        key='SUGGEST_MUNICIPALITIES_BRK',
        defaults={'value': old_value},
    )
    Constance.objects.update_or_create(
        key='SUGGEST_MUNICIPALITIES_BAG',
        defaults={'value': old_value},
    )

class Migration(migrations.Migration):
    dependencies = [
        ('webservice', '0152_map_position_settings'),
        ("constance", "0003_drop_pickle"),
    ]
    
    operations = [
        migrations.RunPython(_migrate_suggest_municipalities),
    ]