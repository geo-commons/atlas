from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0153_migrate_suggest_municipalities'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name='children',
                to='webservice.category',
                verbose_name='Hoofdcategorie',
            ),
        ),
    ]
