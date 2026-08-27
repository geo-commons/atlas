import json

from import_export import resources, fields, widgets
from .models import Category, Source, Layer, Map, Viewer, Metadataset, MapLayer, MapCategory


class CategoryResource(resources.ModelResource):
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=widgets.ForeignKeyWidget(Category, field='slug'))

    class Meta:
        model = Category
        exclude = ('id', )
        import_id_fields = ('slug', )


class MetadatasetResource(resources.ModelResource):
    class Meta:
        model = Metadataset
        exclude = ('id', )
        import_id_fields = ('slug', )


class ViewerResource(resources.ModelResource):
    class Meta:
        model = Viewer
        exclude = ('id', )
        import_id_fields = ('label', )


class LayerResource(resources.ModelResource):
    metadataset = fields.Field(
        column_name='metadataset',
        attribute='metadataset',
        widget=widgets.ForeignKeyWidget(Metadataset, field='slug'))

    layer_source = fields.Field(
        column_name='layer_source',
        attribute='layer_source',
        widget=widgets.ForeignKeyWidget(Source, field='slug'))

    layer_type = fields.Field(
        column_name='layer_type',
        attribute='layer_type',
        widget=widgets.ForeignKeyWidget(Category, field='slug'))

    class Meta:
        model = Layer
        exclude = ('id', 'users', 'atlas_groups')
        import_id_fields = ('slug', )


class SourceResource(resources.ModelResource):
    class Meta:
        model = Source
        exclude = ('id', )
        import_id_fields = ('slug', )


class MapResource(resources.ModelResource):
    layers = fields.Field(column_name='layers')
    categories = fields.Field(column_name='categories')

    class Meta:
        model = Map
        exclude = ('id', )
        import_id_fields = ('slug', )

    def dehydrate_layers(self, obj):
        """Export: Serialize MapLayer relationships with settings, flags, ordering and category."""
        map_layers = MapLayer.objects.filter(map=obj).select_related('layer', 'map_category', 'map_category__category')
        if not map_layers:
            return ''
    
        return '|'.join(
            f"{ml.layer.slug}::{json.dumps(ml.settings)}::{ml.ordering}::"
            f"{ml.map_category.category.slug if ml.map_category else 'no-category'}::{ml.is_base}::{ml.is_visible}"
            for ml in map_layers
        )

    def dehydrate_categories(self, obj):
        """Export: Serialize MapCategory relationships with ordering."""
        map_categories = MapCategory.objects.filter(map=obj).select_related('category')
        if not map_categories:
            return ''
        return '|'.join(
            f"{mc.category.slug}::{mc.ordering}"
            for mc in map_categories
        )

    def after_save_instance(self, instance, row, **kwargs):
        """Import: Create/update MapLayer and MapCategory relationships after Map is saved."""
        super().after_save_instance(instance, row, **kwargs)

        # Handle map categories
        categories_value = row.get('categories', '')
        if categories_value:
            category_data = [item.strip() for item in categories_value.split('|')]

            for item in category_data:
                try:
                    slug, ordering_str = item.split("::", 1)
                    ordering = int(ordering_str)
                except ValueError:
                    slug = item
                    ordering = 0

                try: 
                    category = Category.objects.get(slug=slug)
                except Category.DoesNotExist:
                    continue
                    
                MapCategory.objects.update_or_create(
                    map=instance,
                    category=category,
                    defaults={"ordering": ordering}
                )

        # Handle map layers
        layers_value = row.get('layers', '')
        if layers_value:
            layer_data = [item.strip() for item in layers_value.split('|')]

            for item in layer_data:
                try:
                    slug, settings_json, ordering_str, map_category_slug, is_base_str, is_visible_str = item.split(
                        "::", 5
                    )
                    ordering = int(ordering_str)
                    settings = json.loads(settings_json)
                    is_base = is_base_str == 'True'
                    is_visible = is_visible_str == 'True'
                except ValueError:
                    try:
                        slug, settings_json, ordering_str, map_category_slug = item.split("::", 3)
                        ordering = int(ordering_str)
                        settings = json.loads(settings_json)
                        is_base = bool(settings.pop('is_base', False))
                        is_visible = bool(settings.pop('is_visible', False))
                    except ValueError:
                        slug = item
                        ordering = 0
                        map_category_slug = None
                        settings = {}
                        is_base = False
                        is_visible = False

                map_category = None
                if map_category_slug:
                    try:
                        map_category = MapCategory.objects.get(
                            map=instance,
                            category__slug=map_category_slug
                        )
                    except MapCategory.DoesNotExist:
                        pass

                layer = Layer.objects.filter(slug=slug).first()
                if layer:
                    MapLayer.objects.update_or_create(
                        map=instance,
                        layer=layer,
                        defaults={
                            "settings": settings,
                            "is_base": is_base,
                            "is_visible": is_visible,
                            "ordering": ordering,
                            "map_category": map_category,
                        }
                    )
