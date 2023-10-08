from import_export import resources, fields, widgets
from .models import Category, Source, Layer, Selection, Map


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        exclude = ('id', )
        import_id_fields = ('slug', )


class LayerResource(resources.ModelResource):
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
        exclude = ('id', 'owner', 'users', 'atlas_groups')
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
        widget=widgets.ManyToManyWidget(Layer, field='slug', separator='|'))

    class Meta:
        model = Map
        exclude = ('id', )
        import_id_fields = ('slug', )
