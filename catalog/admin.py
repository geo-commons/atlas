from reversion.admin import VersionAdmin


class TopicAdmin(VersionAdmin):
    list_display = ('title',)
    search_fields = ['title']


class DatasetAdmin(VersionAdmin):
    list_display = ('title', )
    list_filter = ('topics', )
    search_fields = ['title']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'abstract', 'topics', 'data_owner', 'data_administrator')
        }),
        ('Contact', {
            'fields': ('contact_phone', 'contact_address', 'contact_email')
        }),
        ('Actualiteit', {
            'fields': ('update_frequency', 'created_at', 'updated_at')
        }),
        ('Kaartlagen', {
            'fields': ('map_layers', )
        }),
    )
