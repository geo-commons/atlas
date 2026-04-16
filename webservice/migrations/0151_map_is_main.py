from django.db import migrations, models
from django.db.models import Q


MAIN_MAP_FEATURES = {
    'searchbar': True,
    'datapanel': True,
    'selectarea': True,
    'scale': True,
    'measure': True,
    'morepanel': True,
    'layerlist': True,
    'legend': True,
    'baselayer': True,
    'gps': True,
    'zoom': True,
    'markerOnClick': True,
    'resetButton': True,
    'panoramaViewers': True,
}


def create_main_map(apps, schema_editor):
    Map = apps.get_model('webservice', 'Map')
    Layer = apps.get_model('webservice', 'Layer')
    MapLayer = apps.get_model('webservice', 'MapLayer')
    MapCategory = apps.get_model('webservice', 'MapCategory')

    existing_main_map = Map.objects.filter(is_main=True).first()
    if existing_main_map:
        update_fields = []
        if not existing_main_map.published:
            existing_main_map.published = True
            update_fields.append('published')
        if existing_main_map.show_in_overview:
            existing_main_map.show_in_overview = False
            update_fields.append('show_in_overview')
        if update_fields:
            existing_main_map.save(update_fields=update_fields)
        return

    slug = 'hoofdkaart'
    counter = 2
    while Map.objects.filter(slug=slug).exists():
        slug = f'hoofdkaart-{counter}'
        counter += 1

    main_map = Map.objects.create(
        title='Hoofdkaart',
        slug=slug,
        features=MAIN_MAP_FEATURES,
        settings={},
        published=True,
        show_in_overview=False,
        is_main=True,
    )

    visible_layers = Layer.objects.filter(not_in_atlas=False, published=True).order_by('ordering', 'title')
    category_map = {}
    category_ordering = 0

    for ordering, layer in enumerate(visible_layers):
        map_category = None
        if layer.layer_type_id:
            map_category = category_map.get(layer.layer_type_id)
            if map_category is None:
                map_category = MapCategory.objects.create(
                    map=main_map,
                    category_id=layer.layer_type_id,
                    ordering=category_ordering,
                )
                category_map[layer.layer_type_id] = map_category
                category_ordering += 1

        MapLayer.objects.create(
            map=main_map,
            layer=layer,
            map_category=map_category,
            ordering=ordering,
            settings={'customSettings': False},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0150_alter_layer_closed_dataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='is_main',
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text='Markeert deze kaart als de hoofdkaart die op /atlas/ wordt getoond.',
                verbose_name='Hoofdkaart',
            ),
        ),
        migrations.AddConstraint(
            model_name='map',
            constraint=models.UniqueConstraint(
                condition=Q(is_main=True),
                fields=('is_main',),
                name='unique_main_map',
            ),
        ),
        migrations.RunPython(create_main_map, migrations.RunPython.noop),
    ]
