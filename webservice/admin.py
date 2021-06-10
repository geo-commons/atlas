from django.contrib import admin

from .forms import LayerForm, LinkedDataForm
from .models import Category, Layer, AtlasTheme, LinkedData


class LinkedDataInline(admin.TabularInline):
    form = LinkedDataForm
    model = LinkedData
    extra = 1


class LayerAdmin(admin.ModelAdmin):
    form = LayerForm

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset',
                    'published')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    list_filter = ('layer_type', 'closed_dataset')

    inlines = [
        LinkedDataInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('title', 'layer_id', 'layer_type', 'published')
        }),
        ('Bron', {
            'fields': ('layer_name', 'url', 'source_type', 'projection', 'server_type')
        }),
        ('Weergave', {
            'fields': ('opacity', 'is_base', 'is_visible', 'not_in_atlas', 'isqueryable', '_popup_attributes', '_search_fields')
        }),
        ('Metadata', {
            'fields': ('meta_name', 'meta_kind', 'meta_org', 'meta_updated')
        }),
        ('Toegang', {
            'fields': ('closed_dataset', 'owner', 'users', 'atlas_groups')
        })
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'title')
    list_display_links = ('title',)
    list_editable = ('ordering',)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AtlasTheme, ThemeAdmin)
