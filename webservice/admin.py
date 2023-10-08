from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats
from .forms import LayerForm, LinkedDataForm
from .models import Source, Category, Layer, Template, Selection, Map, LinkedData, Viewer
from .resources import CategoryResource, LayerResource, SourceResource, SelectionResource, MapResource


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


class CustomImportExportActionModelAdmin(ImportExportActionModelAdmin):
    def get_export_formats(self):
        formats = (
            base_formats.JSON,
        )

        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        formats = (
            base_formats.JSON,
        )

        return [f for f in formats if f().can_import()]

    class Meta:
        abstract = True


class SourceAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title',)
    resource_classes = [SourceResource]
    filter_horizontal = ('atlas_groups', )


class LayerAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    form = LayerForm

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset', 'login_required',
                    'published')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    list_filter = ('layer_type', 'closed_dataset', 'login_required')

    filter_horizontal = ('atlas_groups', )

    actions = [duplicate_layer]

    resource_classes = [LayerResource]

    inlines = [
        LinkedDataInline,
        TemplateInline,
    ]

    save_as = True

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'layer_type', 'published')
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
            'fields': ('meta_name', 'meta_description', 'meta_org', 'meta_updated', 'meta_link', 'owner')
        }),
        ('Toegang', {
            'fields': ('closed_dataset', 'login_required', 'atlas_groups')
        })
    )

    search_fields = ['title']


class CategoryAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('ordering', 'title')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    search_fields = ['title']
    resource_classes = [CategoryResource]


class SelectionAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title', )
    fields = ('title', 'slug', 'layers', 'login_required')
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('layers', )

    search_fields = ['title']
    resource_classes = [SelectionResource]


class MapAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title', )
    fields = ('title', 'slug', 'layers', 'features', 'settings')
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('layers', )

    search_fields = ['title']
    resource_classes = [MapResource]


class ViewerAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('ordering', 'label', 'type', )
    list_display_links = ('label',)
    list_editable = ('ordering',)


admin.site.register(Source, SourceAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Viewer, ViewerAdmin)
