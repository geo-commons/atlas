from import_export import resources

from authz.models import Authorization


class AuthorizationResource(resources.ModelResource):
    class Meta:
        model = Authorization
        exclude = ('id', )
        import_id_fields = ('resource', )