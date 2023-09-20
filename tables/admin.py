from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Table


class TableAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('ordering', 'title', )
    list_display_links = ('title',)
    list_editable = ('ordering',)


admin.site.register(Table, TableAdmin)
