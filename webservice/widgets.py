import json

from import_export import widgets
from webservice.models import Map


class MapLayerManyToManyWidget(widgets.ManyToManyWidget):
    """
    Custom widget to handle ManyToMany relationships through the MapLayer model.
    """
    def __init__(self, model, through_model, map_field, layer_field, field='slug', separator='|'): # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(model, field=field, separator=separator)
        self.through_model = through_model
        self.map_field = map_field
        self.layer_field = layer_field

    def clean(self, value, row=None, *args, **kwargs): # pylint: disable=keyword-arg-before-vararg
        """
        Parses the input string of Layer Slugs and ensures MapLayer instances are created,
        including the `settings` JSON field.
        """
        if not value:
            return []

        # Get the map instance
        try:
            map_instance = Map.objects.get(slug=row['slug']) if 'slug' in row else None
        except Map.DoesNotExist:
            return []

        if not map_instance:
            return []

        layer_data = [item.strip() for item in value.split(self.separator)]
        layers = []

        for item in layer_data:
            try:
                slug, settings_json = item.split(":", 1)  # Extract slug and settings
                settings = json.loads(settings_json)  # Convert JSON string to dict
            except ValueError:
                slug = item  # If there's no settings JSON, just use the slug
                settings = {}  # Default to empty settings

            layer = self.model.objects.filter(slug=slug).first()
            if layer:
                layers.append(layer)
                self.through_model.objects.get_or_create(
                    **{self.map_field: map_instance, self.layer_field: layer},
                    defaults={"settings": settings}  # Ensure settings are set
                )

        return layers

    def render(self, value, obj=None):
        """
        Serializes the ManyToManyField for export.
        """
        if not value:
            return ''

        map_instance = obj
        map_layers = self.through_model.objects.filter(**{self.map_field: map_instance})

        return self.separator.join(
            f"{layer.layer.slug}:{json.dumps(layer.settings)}" for layer in map_layers
        )