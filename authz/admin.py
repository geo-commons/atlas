from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Authorization, Log


class AuthorizationAdmin(VersionAdmin):
    list_display = ('ordering', 'resource', 'source', 'description')
    list_display_links = ('resource', )
    list_editable = ('ordering',)
    list_filter = ('resource', 'source')
    filter_horizontal = ('atlas_groups', )


class LogAdmin(admin.ModelAdmin):
    list_display = ('time_created', 'username', 'source', 'resource', )
    list_display_links = ('time_created',)
    list_filter = ('time_created', 'source', 'resource', 'username')

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'ip', 'user_agent')
        }),
        ('Log', {
            'fields': (
                'source',
                'resource',
                'params'
            )
        }),
    )

    def has_add_permission(self, _request, _obj=None):
        return False

    def has_delete_permission(self, _request, _obj=None):
        return False

    def has_change_permission(self, _request, _obj=None):
        return False


admin.site.register(Authorization, AuthorizationAdmin)
admin.site.register(Log, LogAdmin)
