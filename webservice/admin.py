from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .forms import LayerForm, LinkedDataForm
from .models import Source, Category, Layer, Template, Map, LinkedData, Viewer
from .resources import CategoryResource, LayerResource, SourceResource, MapResource


class SourceAdmin(ImportExportActionModelAdmin):
    list_display = ('title',)
    resource_classes = [SourceResource]


class LinkedDataInline(admin.TabularInline):
    form = LinkedDataForm
    model = LinkedData
    extra = 0


class TemplateInline(admin.StackedInline):
    model = Template
    extra = 0


@admin.action(description='Geselecteerde kaartlagen dupliceren')
def duplicate_layer(_modeladmin, _request, queryset):
    for layer in queryset.all():
        layer.pk = None
        layer.published = False

        i = 2
        while Layer.objects.filter(title=f'{layer.title} ({i})').count() > 0:
            i += 1

        layer.title = f'{layer.title} ({i})'
        layer.save()


class LayerAdmin(ImportExportActionModelAdmin):
    form = LayerForm

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset',
                    'published')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    list_filter = ('layer_type', 'closed_dataset')

    actions = [duplicate_layer]

    resource_classes = [LayerResource]

    inlines = [
        LinkedDataInline,
        TemplateInline,
    ]

    save_as = True

    fieldsets = (
        (None, {
            'fields': ('title', 'layer_id', 'layer_type', 'published')
        }),
        ('Bron', {
            'fields': ('layer_source', 'layer_name', 'source_type', 'projection', 'server_type', 'format')
        }),
        ('Weergave', {
            'fields': (
                'opacity',
                'is_base',
                'is_visible',
                'is_selectable',
                'show_in_detail_panel',
                'not_in_atlas',
                '_popup_attributes',
                '_search_fields',
                'extent_min_x',
                'extent_min_y',
                'extent_max_x',
                'extent_max_y',
                'zoom_min',
                'zoom_max',
                'server_style',
                'client_style',
                'friendly_fields'
            )
        }),
        ('Metadata', {
            'fields': ('meta_name', 'meta_description', 'meta_org', 'meta_updated', 'meta_link')
        }),
        ('Toegang', {
            'fields': ('closed_dataset', 'login_required', 'owner', 'users', 'atlas_groups')
        })
    )

    prepopulated_fields = {'layer_id': ('title', )}

    search_fields = ['title']


class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ('ordering', 'title')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    search_fields = ['title']
    resource_classes = [CategoryResource]


class MapAdmin(ImportExportActionModelAdmin):
    list_display = ('title', )
    fields = ('title', 'slug', 'layers', 'features', 'settings')
    prepopulated_fields = {'slug': ('title', )}

    search_fields = ['title']
    resource_classes = [MapResource]


class ViewerAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'label', 'type', )
    list_display_links = ('label',)
    list_editable = ('ordering',)


admin.site.register(Source, SourceAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Viewer, ViewerAdmin)
