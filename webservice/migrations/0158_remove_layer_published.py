from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0157_metadataset_fme_script_alter_metadataset_abstract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layer',
            name='published',
        ),
    ]
