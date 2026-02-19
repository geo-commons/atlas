# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0019_alter_table_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='thumbnail',
        ),
    ]
