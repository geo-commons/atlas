from import_export import resources, fields, widgets
from .models import Category, Source, Layer, Selection, Map, Theme, Viewer, Dataset, MapLayer
from .widgets import MapLayerManyToManyWidget


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        exclude = ('id', )
        import_id_fields = ('slug', )


class ThemeResource(resources.ModelResource):
    class Meta:
        model = Theme
        exclude = ('id', )
        import_id_fields = ('slug', )


class DatasetResource(resources.ModelResource):
    class Meta:
        model = Dataset
        exclude = ('id', )
        import_id_fields = ('slug', )


class ViewerResource(resources.ModelResource):
    class Meta:
        model = Viewer
        exclude = ('id', )
        import_id_fields = ('label', )


class LayerResource(resources.ModelResource):
    layer_source = fields.Field(
        column_name='layer_source',
        attribute='layer_source',
        widget=widgets.ForeignKeyWidget(Source, field='slug'))

    layer_type = fields.Field(
        column_name='layer_type',
        attribute='layer_type',
        widget=widgets.ForeignKeyWidget(Category, field='slug'))

    dataset = fields.Field(
        column_name='dataset',
        attribute='dataset',
        widget=widgets.ForeignKeyWidget(Dataset, field='slug')
    )

    class Meta:
        model = Layer
        exclude = ('id', 'users', 'atlas_groups')
        import_id_fields = ('slug', )


class SourceResource(resources.ModelResource):
    class Meta:
        model = Source
        exclude = ('id', )
        import_id_fields = ('slug', )


class SelectionResource(resources.ModelResource):
    layers = fields.Field(
        column_name='layers',
        attribute='layers',
        widget=widgets.ManyToManyWidget(Layer, field='slug', separator='|'))

    class Meta:
        model = Selection
        exclude = ('id', )
        import_id_fields = ('slug', )


class MapResource(resources.ModelResource):
    layers = fields.Field(
        column_name='layers',
        attribute='layers',
        widget=MapLayerManyToManyWidget(
            model=Layer,
            through_model=MapLayer,
            map_field='map',
            layer_field='layer',
            field='slug',
            separator='|'
        )
    )

    class Meta:
        model = Map
        exclude = ('id', )
        import_id_fields = ('slug', )
