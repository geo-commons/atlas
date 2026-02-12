from import_export import resources

from table.models import Table

class TableResource(resources.ModelResource):
    class Meta:
        model = Table
        exclude = ('id', 'tables', 'layers')
        import_id_fields = ('slug', )