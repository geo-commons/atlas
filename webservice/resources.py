from import_export import resources
from .models import Category, Source, Layer, Map


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class LayerResource(resources.ModelResource):
    class Meta:
        model = Layer


class SourceResource(resources.ModelResource):
    class Meta:
        model = Source


class MapResource(resources.ModelResource):
    class Meta:
        model = Map
