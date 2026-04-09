from django.db import transaction

from webservice.models import Layer, Map, MapCategory, MapLayer


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


def _get_available_slug() -> str:
    slug = 'hoofdkaart'
    counter = 2

    while Map.objects.filter(slug=slug).exists():
        slug = f'hoofdkaart-{counter}'
        counter += 1

    return slug


@transaction.atomic
def ensure_main_map() -> tuple[Map, bool]:
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

        return existing_main_map, False

    main_map = Map.objects.create(
        title='Hoofdkaart',
        slug=_get_available_slug(),
        features=MAIN_MAP_FEATURES.copy(),
        settings={},
        published=True,
        show_in_overview=False,
        is_main=True,
    )

    visible_layers = Layer.objects.filter(not_in_atlas=False, published=True).order_by('ordering', 'title')
    map_categories_by_category_id = {}
    category_ordering = 0

    for ordering, layer in enumerate(visible_layers):
        map_category = None

        if layer.layer_type_id:
            map_category = map_categories_by_category_id.get(layer.layer_type_id)

            if map_category is None:
                map_category = MapCategory.objects.create(
                    map=main_map,
                    category_id=layer.layer_type_id,
                    ordering=category_ordering,
                )
                map_categories_by_category_id[layer.layer_type_id] = map_category
                category_ordering += 1

        MapLayer.objects.create(
            map=main_map,
            layer=layer,
            map_category=map_category,
            ordering=ordering,
            settings={'customSettings': False},
        )

    return main_map, True
