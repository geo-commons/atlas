from import_export import resources

from tables.models import Table


class TableResource(resources.ModelResource):
    class Meta:
        model = Table
        exclude = ('id', )
        import_id_fields = ('slug', )