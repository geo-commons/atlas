def create_map_categories(apps, schema_editor):
    Map = apps.get_model('webservice', 'Map')
    MapCategory = apps.get_model('webservice', 'MapCategory')
    MapLayer = apps.get_model('webservice', 'MapLayer')
    
    for map_instance in Map.objects.all():
        # Get unique categories from map's layers
        categories = set()
        for map_layer in map_instance.map_layers.all():
            category = map_layer.layer.layer_type

            if category:
                categories.add(category)
        
        # Create MapCategory for each unique category
        for idx, category in enumerate(sorted(categories, key=lambda category: category.ordering)):
            map_category, created = MapCategory.objects.get_or_create(
                map=map_instance,
                category=category,
                defaults={'ordering': idx}
            )
            
            # Associate MapLayers with their MapCategory
            map_layers = MapLayer.objects.filter(
                map=map_instance,
                layer__layer_type=category
            )

            for layer_idx, map_layer in enumerate(sorted(map_layers, key=lambda map_layer: map_layer.layer.ordering)):
                map_layer.map_category = map_category
                map_layer.ordering = layer_idx
                map_layer.save()
