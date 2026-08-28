from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0158_remove_layer_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='disable_highlighted_style',
            field=models.BooleanField(default=False, verbose_name='Geselecteerde objecten niet highlighten'),
        ),
    ]
